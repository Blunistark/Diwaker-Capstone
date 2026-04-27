import RPi.GPIO as GPIO
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import PINS
from sensors.moisture_sensor import MoistureSensor

def test_moisture():
    GPIO.setmode(GPIO.BCM)
    moisture = MoistureSensor(PINS["SENSORS"]["MOISTURE_DIGITAL"])
    print("Testing Moisture Sensor... Press Ctrl+C to stop.")
    try:
        while True:
            if moisture.is_wet():
                print("Status: WET")
            else:
                print("Status: DRY")
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    test_moisture()
