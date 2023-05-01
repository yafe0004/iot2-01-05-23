from flask import Flask, render_template
from datetime import datetime
from time import sleep
import RPi.GPIO as GPIO
import sqlite3
import data

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

# Create a Flask app:
app = Flask(__name__)

@app.route('/')
def index():
    data.ir_sensor_er()
    IR_sensor_one_value = GPIO.input(IR_Sensor_one)
    IR_sensor_two_value = GPIO.input(IR_Sensor_two)
    IR_sensor_three_value = GPIO.input(IR_Sensor_three)
    IR_sensor_four_value = GPIO.input(IR_Sensor_four)
    print(IR_sensor_one_value)
    print(IR_sensor_two_value)
    print(IR_sensor_three_value)
    print(IR_sensor_four_value)
    return render_template('hjemløs.html')
    
 
if __name__ == "__main__":
    # Run the app on the local server:
    app.run(host='192.168.137.36', port=8000, debug=True)
