import RPi.GPIO as GPIO
import time

class ServoMotor:
    """
    Handles waste redirection using servo motors.
    """
    def __init__(self, pin):
        self.pin = pin
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50) # 50Hz frequency
        self.pwm.start(0)

    def set_angle(self, angle):
        """
        Sets the servo to a specific angle (0-180).
        """
        duty = angle / 18 + 2
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.pwm.stop()
