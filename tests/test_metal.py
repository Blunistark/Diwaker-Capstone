import RPi.GPIO as GPIO
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import PINS
from sensors.metal_sensor import MetalSensor

def test_metal():
    GPIO.setmode(GPIO.BCM)
    metal = MetalSensor(PINS["SENSORS"]["METAL_DETECTION"])
    print("Testing Metal Sensor... Press Ctrl+C to stop.")
    try:
        while True:
            if metal.is_metal():
                print("Status: METAL DETECTED")
            else:
                print("Status: NO METAL")
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    test_metal()
