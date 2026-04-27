import RPi.GPIO as GPIO
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import PINS
from sensors.ultrasonic_sensor import UltrasonicSensor

def test_ultrasonic():
    GPIO.setmode(GPIO.BCM)
    ultrasonic = UltrasonicSensor(PINS["SENSORS"]["ULTRASONIC"]["TRIG"], PINS["SENSORS"]["ULTRASONIC"]["ECHO"])
    print("Testing Ultrasonic Sensor... Press Ctrl+C to stop.")
    try:
        while True:
            dist = ultrasonic.get_distance()
            print(f"Distance: {dist:.2f} cm")
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    test_ultrasonic()
