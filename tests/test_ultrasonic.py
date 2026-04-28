import RPi.GPIO as GPIO
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import PINS
from sensors.ultrasonic_sensor import UltrasonicSensor

def test_ultrasonic():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Initialize both sensors
    print("Initializing sensors...")
    sensor_wet = UltrasonicSensor(
        PINS["SENSORS"]["ULTRASONIC_WET"]["TRIG"], 
        PINS["SENSORS"]["ULTRASONIC_WET"]["ECHO"]
    )
    sensor_metaldry = UltrasonicSensor(
        PINS["SENSORS"]["ULTRASONIC_METALDRY"]["TRIG"], 
        PINS["SENSORS"]["ULTRASONIC_METALDRY"]["ECHO"]
    )
    
    print("Testing Dual Ultrasonic Sensors... Press Ctrl+C to stop.")
    print("-" * 40)
    
    try:
        while True:
            dist_wet = sensor_wet.get_distance()
            dist_metaldry = sensor_metaldry.get_distance()
            
            print(f"Wet Bin: {dist_wet:6.2f} cm | Metal/Dry Bin: {dist_metaldry:6.2f} cm")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nCleaning up...")
        GPIO.cleanup()

if __name__ == "__main__":
    test_ultrasonic()
