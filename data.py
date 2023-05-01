import sqlite3
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep

# Set the pin numbers for the sensors:
IR_Sensor_one = 23
IR_Sensor_two = 16
IR_Sensor_three = 26
IR_Sensor_four = 24

# Set the mode for GPIO pin numbering:
GPIO.setmode(GPIO.BCM)

# Set the input pins as pull-downs:
GPIO.setup(IR_Sensor_one, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IR_Sensor_two, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IR_Sensor_three, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IR_Sensor_four, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def ir_sensor_er():
     # Opret forbindelse til databasen
    conn = sqlite3.connect('group2_database.db')  # Erstatt 'ny_database.db' med det navn, du vil give din nye database
    # Læs sensor data
    ir_sensor_one_value = GPIO.input(IR_Sensor_one)
    ir_sensor_two_value = GPIO.input(IR_Sensor_two)
    ir_sensor_three_value = GPIO.input(IR_Sensor_three)
    ir_sensor_four_value = GPIO.input(IR_Sensor_four)
    # Opret en tabel til sensor data
    conn.execute('''CREATE TABLE IF NOT EXISTS sensor_data (timestamp TEXT, sensor_name TEXT, sensor_value REAL)''')
    conn.commit()
   
    # Indsæt data i databasen
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute("INSERT INTO sensor_data VALUES (?, ?, ?)", (timestamp, "IR_Sensor_one", ir_sensor_one_value))
    conn.execute("INSERT INTO sensor_data VALUES (?, ?, ?)", (timestamp, "IR_Sensor_two", ir_sensor_two_value))
    conn.execute("INSERT INTO sensor_data VALUES (?, ?, ?)", (timestamp, "IR_Sensor_three", ir_sensor_three_value))
    conn.execute("INSERT INTO sensor_data VALUES (?, ?, ?)", (timestamp, "IR_Sensor_four", ir_sensor_four_value))
    conn.commit()

    # Print sensor data
    print("IR Sensor one: ", ir_sensor_one_value)
    print("IR Sensor two: ", ir_sensor_two_value)
    print("IR Sensor three: ", ir_sensor_three_value)
    print("IR Sensor four: ", ir_sensor_four_value)

    sleep(0.2)

