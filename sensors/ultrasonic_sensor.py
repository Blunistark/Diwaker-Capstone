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
        Returns the distance measured in cm. Includes a timeout to prevent hanging.
        """
        # Ensure trig pin is low
        GPIO.output(self.trig_pin, False)
        time.sleep(0.1)

        # Send 10us pulse
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

        start_time = time.time()
        stop_time = time.time()
        timeout = start_time + 0.1 # 100ms timeout

        # Wait for ECHO to go HIGH
        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()
            if start_time > timeout:
                return -1 # Timeout error

        # Wait for ECHO to go LOW
        timeout = start_time + 0.1
        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()
            if stop_time > timeout:
                return -1 # Timeout error

        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2

        # Filter out unrealistic values
        if distance > 400 or distance < 2:
            return 0
            
        return distance

    def get_fill_percentage(self, bin_height_cm):
        """
        Calculates fill percentage based on bin height and distance.
        """
        dist = self.get_distance()
        if dist > bin_height_cm:
            return 0
        return ((bin_height_cm - dist) / bin_height_cm) * 100
