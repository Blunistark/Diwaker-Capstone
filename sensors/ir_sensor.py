import RPi.GPIO as GPIO

class IRSensor:
    """
    Handles waste detection using the IR Sensor with hardware interrupts.
    """
    def __init__(self, pin):
        self.pin = pin
        # Use internal pull-up for stability
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Add event detection for falling edge (Object detection)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, bouncetime=200)

    def is_waste_detected(self):
        """
        Returns True if waste has been detected since the last check.
        Using event_detected() captures pulses that happen while the Pi is busy.
        """
        return GPIO.event_detected(self.pin)
