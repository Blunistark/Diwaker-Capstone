import RPi.GPIO as GPIO

class MoistureSensor:
    """
    Handles classification of wet vs dry waste.
    """
    def __init__(self, digital_pin, analog_channel=None):
        self.digital_pin = digital_pin
        self.analog_channel = analog_channel
        # Use internal pull-up to keep the pin HIGH (Dry) when not triggered
        GPIO.setup(self.digital_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_wet(self):
        """
        Returns True if the waste is classified as wet.
        Most digital moisture sensors output LOW when wet.
        """
        return GPIO.input(self.digital_pin) == GPIO.LOW
