import RPi.GPIO as GPIO

class IRSensor:
    """
    Handles waste detection using the IR Sensor with hardware interrupts.
    """
    def __init__(self, pin):
        self.pin = pin
        # Ensure pin is set to INPUT with Pull-up
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Clean up any existing detection to prevent "Failed to add edge detection"
        try:
            GPIO.remove_event_detect(self.pin)
        except:
            pass
            
        # Add event detection for falling edge (Object detection)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, bouncetime=200)

    def is_waste_detected(self):
        """
        Returns True if waste has been detected since the last check.
        """
        return GPIO.event_detected(self.pin)
