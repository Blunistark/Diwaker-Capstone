import RPi.GPIO as GPIO
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import PINS
from actuators.servo_motor import ServoMotor

def test_servo():
    GPIO.setmode(GPIO.BCM)
    servo = ServoMotor(PINS["ACTUATORS"]["SERVO_MAIN"])
    print("Testing Servo Motor (Sweep)... Press Ctrl+C to stop.")
    try:
        while True:
            print("Angle: 0")
            servo.set_angle(0)
            time.sleep(1)
            print("Angle: 90")
            servo.set_angle(90)
            time.sleep(1)
            print("Angle: 180")
            servo.set_angle(180)
            time.sleep(1)
    except KeyboardInterrupt:
        servo.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    test_servo()
