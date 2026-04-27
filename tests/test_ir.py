import RPi.GPIO as GPIO
import time
import sys
import os

# Add parent directory to path to import local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import PINS
from sensors.ir_sensor import IRSensor

def test_ir():
    GPIO.setmode(GPIO.BCM)
    ir = IRSensor(PINS["SENSORS"]["IR_DETECTION"])
    print("Testing IR Sensor... Press Ctrl+C to stop.")
    try:
        while True:
            if ir.is_waste_detected():
                print("Waste Detected!")
            else:
                print("No Waste.")
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    test_ir()
