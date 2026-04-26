import RPi.GPIO as GPIO

class MetalSensor:
    """
    Handles detection of metallic waste.
    """
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def is_metal(self):
        """
        Returns True if metallic waste is detected.
        """
        # Metal sensors typically output HIGH or LOW based on inductive sensing
        return GPIO.input(self.pin) == GPIO.HIGH
