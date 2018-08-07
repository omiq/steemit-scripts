import serial
import time
from datetime import datetime

print("Starting ...")

# change the port to whichever shows in Arduino
tardis = serial.Serial('/dev/ttyACM0', baudrate=9600)

while(1):
    tardis.write(str(datetime.now()).encode())
    time.sleep(10)
