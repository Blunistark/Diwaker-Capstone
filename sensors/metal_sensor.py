import RPi.GPIO as GPIO

class MetalSensor:
    """
    Handles detection of metallic waste.
    """
    def __init__(self, pin):
        self.pin = pin
        # Using pull-up for 2-pin switch-type modules
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_metal(self):
        """
        Returns True if metallic waste is detected.
        """
        # Triggers when pin is pulled to GND
        return GPIO.input(self.pin) == GPIO.LOW
