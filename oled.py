import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Initialiser I2C-bussen og SSD1306 OLED-displayet
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Ryd displayet
oled.fill(0)
oled.show()

# Sæt tekstfarve og font
font = ImageFont.load_default()
farve = 255

# Opret billedobjekt og tegneobjekt
billede = Image.new("1", (oled.width, oled.height))
tegn = ImageDraw.Draw(billede)

def IR_sensorer(IR_sensor_en, IR_sensor_to, IR_sensor_tre, IR_sensor_fire):
    while True:
        # Tjek om alle IR-sensorer er dækket
        if IR_sensor_en == 1 and IR_sensor_to == 1 and IR_sensor_tre == 1 and IR_sensor_fire == 1:
            # Vis besked på OLED-displayet
            tegn.text((1, 1), "Skraldspand skal tømmes!", font=font, fill=farve)
            oled.image(billede)
            oled.show()

        # Tjek om en hvilken som helst IR-sensor ikke er dækket
        elif IR_sensor_en == 0 and IR_sensor_to == 0 and IR_sensor_tre == 0 and IR_sensor_fire == 0:
            # Vis besked på OLED-displayet
            tegn.text((0, 0), "Skraldspand er ikke fyldt", font=font, fill=farve)
            oled.image(billede)
            oled.show()

        # Vent i et sekund, før der tjekkes igen
        time.sleep(1)

# Kald IR_sensorer funktionen med sample værdier
IR_sensorer(0, 0, 0, 0)
