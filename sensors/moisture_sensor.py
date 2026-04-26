import RPi.GPIO as GPIO

class MoistureSensor:
    """
    Handles classification of wet vs dry waste.
    """
    def __init__(self, digital_pin, analog_channel=None):
        self.digital_pin = digital_pin
        self.analog_channel = analog_channel
        GPIO.setup(self.digital_pin, GPIO.IN)

    def is_wet(self):
        """
        Returns True if the waste is classified as wet.
        """
        # Digital output typically goes LOW when moisture is detected
        return GPIO.input(self.digital_pin) == GPIO.LOW

    def get_moisture_level(self):
        """
        Optional: Read analog value if using an ADC (like MCP3008).
        """
        if self.analog_channel is not None:
            # Logic for reading from ADC would go here
            return 0 
        return None
