import RPi.GPIO as GPIO

class IRSensor:
    """
    Handles waste detection using the IR Sensor.
    """
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def is_waste_detected(self):
        """
        Returns True if waste is detected in front of the sensor.
        """
        # IR sensors typically output LOW when an object is detected
        return GPIO.input(self.pin) == GPIO.LOW
