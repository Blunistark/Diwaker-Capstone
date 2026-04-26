import RPi.GPIO as GPIO
import time
from config import PINS, IOT_CONFIG, THRESHOLDS
from sensors.ir_sensor import IRSensor
from sensors.moisture_sensor import MoistureSensor
from sensors.metal_sensor import MetalSensor
from sensors.ultrasonic_sensor import UltrasonicSensor
from actuators.servo_motor import ServoMotor
from iot.cloud_client import CloudClient

def main():
    # Setup GPIO mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Initialize Sensors
    ir_sensor = IRSensor(PINS["SENSORS"]["IR_DETECTION"])
    moisture_sensor = MoistureSensor(PINS["SENSORS"]["MOISTURE_DIGITAL"])
    metal_sensor = MetalSensor(PINS["SENSORS"]["METAL_DETECTION"])
    
    ultrasonic_wet = UltrasonicSensor(PINS["SENSORS"]["ULTRASONIC_WET"]["TRIG"], PINS["SENSORS"]["ULTRASONIC_WET"]["ECHO"])
    ultrasonic_dry = UltrasonicSensor(PINS["SENSORS"]["ULTRASONIC_DRY"]["TRIG"], PINS["SENSORS"]["ULTRASONIC_DRY"]["ECHO"])
    ultrasonic_metal = UltrasonicSensor(PINS["SENSORS"]["ULTRASONIC_METAL"]["TRIG"], PINS["SENSORS"]["ULTRASONIC_METAL"]["ECHO"])

    # Initialize Actuators
    servo = ServoMotor(PINS["ACTUATORS"]["SERVO_MAIN"])

    # Initialize IoT Client
    cloud = CloudClient(IOT_CONFIG)
    cloud.connect()

    print("Waste Segregation System Started...")

    try:
        while True:
            # 1. Monitoring Bin Levels
            fill_levels = {
                "wet": ultrasonic_wet.get_fill_percentage(30), # Assuming 30cm bin height
                "dry": ultrasonic_dry.get_fill_percentage(30),
                "metal": ultrasonic_metal.get_fill_percentage(30)
            }

            # 2. Detection and Segregation Logic
            if ir_sensor.is_waste_detected():
                print("Waste Detected! Classifying...")
                time.sleep(1) # Wait for sensors to stabilize

                waste_type = "dry" # Default
                
                if metal_sensor.is_metal():
                    waste_type = "metal"
                    servo.set_angle(120) # Move to metal bin
                elif moisture_sensor.is_wet():
                    waste_type = "wet"
                    servo.set_angle(60) # Move to wet bin
                else:
                    servo.set_angle(0) # Move to dry bin

                print(f"Classified as: {waste_type}")
                
                # Update Cloud
                cloud.publish_status(fill_levels, waste_type)
                time.sleep(2) # Wait for waste to drop
                servo.set_angle(90) # Return to idle position

            # Periodic Status Update
            cloud.publish_status(fill_levels, "none")
            time.sleep(5)

    except KeyboardInterrupt:
        print("System shutting down...")
    finally:
        GPIO.cleanup()
        cloud.disconnect()

if __name__ == "__main__":
    main()
