import RPi.GPIO as GPIO

class MetalSensor:
    """
    Handles detection of metallic waste.
    """
    def __init__(self, pin):
        self.pin = pin
        # Using pull-down for 2-pin series-type modules (3.3V -> Sensor -> Pin)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_metal(self):
        """
        Returns True if metallic waste is detected.
        """
        # Triggers when the sensor closes the circuit to 3.3V
        return GPIO.input(self.pin) == GPIO.HIGH
