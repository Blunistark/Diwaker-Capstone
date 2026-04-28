import RPi.GPIO as GPIO
import time

class IRSensor:
    """
    Handles waste detection using the IR Sensor with hardware interrupts.
    """
    def __init__(self, pin):
        self.pin = pin
        
        # Aggressive cleanup for this specific pin
        try:
            GPIO.remove_event_detect(self.pin)
            time.sleep(0.1) # Give the kernel a moment to release the pin
        except:
            pass
            
        # Ensure pin is set to INPUT with Pull-up
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Try to add event detection
        try:
            GPIO.add_event_detect(self.pin, GPIO.FALLING, bouncetime=200)
        except RuntimeError as e:
            print(f"Warning: Falling edge detection failed ({e}). Falling back to simple polling.")
            # We don't raise the error, so the script can still run in polling mode

    def is_waste_detected(self):
        """
        Returns True if waste is detected. 
        Uses interrupt if available, otherwise falls back to direct reading.
        """
        try:
            # Try interrupt-based detection first
            if GPIO.event_detected(self.pin):
                return True
        except:
            pass
            
        # Fallback: Direct real-time check (less sensitive but works if interrupt fails)
        return GPIO.input(self.pin) == GPIO.LOW
