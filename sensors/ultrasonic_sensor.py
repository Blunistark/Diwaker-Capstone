import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    """
    Handles bin fill level monitoring.
    """
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        """
        Returns the distance measured in cm. Includes debug prints.
        """
        for _ in range(3):
            GPIO.output(self.trig_pin, False)
            time.sleep(0.1)

            GPIO.output(self.trig_pin, True)
            time.sleep(0.00002)
            GPIO.output(self.trig_pin, False)

            start_time = time.time()
            stop_time = time.time()
            timeout = start_time + 1.0 # Increased to 1 second

            # Wait for ECHO to go HIGH
            while GPIO.input(self.echo_pin) == 0:
                start_time = time.time()
                if start_time > timeout:
                    print("Debug: Sensor Timeout - ECHO never went HIGH")
                    break
            else:
                # Wait for ECHO to go LOW
                timeout = start_time + 1.0
                while GPIO.input(self.echo_pin) == 1:
                    stop_time = time.time()
                    if stop_time > timeout:
                        print("Debug: Sensor Timeout - ECHO never went LOW")
                        break
                else:
                    time_elapsed = stop_time - start_time
                    distance = (time_elapsed * 34300) / 2
                    if 2 <= distance <= 400:
                        return distance
        
        return -1

    def get_fill_percentage(self, bin_height_cm):
        """
        Calculates fill percentage based on bin height and distance.
        """
        dist = self.get_distance()
        if dist > bin_height_cm:
            return 0
        return ((bin_height_cm - dist) / bin_height_cm) * 100
