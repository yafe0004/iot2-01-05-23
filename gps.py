import serial
import pynmea2
import sqlite3
import RPi.GPIO as GPIO
import time
from flask import Flask



app = Flask(__name__)


# Sæt tilstandene for GPIO-pinnumrene:
GPIO.setmode(GPIO.BCM)
Tx_Rx_gps = 14
Rx_Tx_gps = 15



# Opret forbindelse til serielt port til GPS-modulet
port = "/dev/ttyAMA0"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)

# Opret forbindelse til SQLite-databasen
conn = sqlite3.connect('gps_data.db')
c = conn.cursor()

# Opret GPS-data-tabellen, hvis den ikke allerede findes
c.execute('''CREATE TABLE IF NOT EXISTS gps_data
             (time text, latitude real, longitude real, altitude real)''')

# Definer GPIO-pins til LED og GPS
Rx_Tx_gps = 15
GPIO.setup(Rx_Tx_gps, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Funktion til at hente GPS-data og gemme dem i databasen
def get_gps_data():
    # Hent nuværende tidspunkt
    time_stamp = time.strftime('%Y-%m-%d %H:%M:%S')

    while True:
        newdata = ser.readline().decode("unicode_escape")
        if newdata[0:6] == "$GPGGA":
            newmsg = pynmea2.parse(newdata)
            latitude = newmsg.latitude
            longitude = newmsg.longitude
            altitude = newmsg.altitude
            print("Breddegrad={}, Længdegrad={}, Højde={}".format(latitude, longitude, altitude))

            # Indsæt GPS-data i databasen
            c.execute("INSERT INTO gps_data VALUES (?, ?, ?, ?)", (time_stamp, latitude, longitude, altitude))
            conn.commit()
            break

    # Vent på den næste GPS-data
    time.sleep(1)

# Flask-rute for at vise GPS-positionen
@app.route('/gps')
def gps():
    # Tjek GPS-status
    Rx_Tx_gps_value = GPIO.input(Rx_Tx_gps)
        
 
    if Rx_Tx_gps_value:
        # Hent den seneste GPS-position fra databasen
        c.execute("SELECT * FROM gps_data ORDER BY time DESC LIMIT 1")
        latest_data = c.fetchone()
        latitude = latest_data[1]
        longitude = latest_data[2]
        altitude = latest_data[3]
        return f"GPS position: Latitude={latitude}, Longitude={longitude}, Altitude={altitude}"
    else:
        return "No GPS signal"
    
    
   

if __name__ == "__main__":
    # Kør appen på den lokale server:
    app.run(host='192.168.137.36', port=8000, debug=True)
    # Mål GPS-data og gem dem i databasen
    while True:
        get_gps_data()


