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
    
    # Using a single ultrasonic sensor for overall monitoring
    ultrasonic = UltrasonicSensor(PINS["SENSORS"]["ULTRASONIC"]["TRIG"], PINS["SENSORS"]["ULTRASONIC"]["ECHO"])

    # Initialize Actuator
    servo = ServoMotor(PINS["ACTUATORS"]["SERVO_MAIN"])
    servo.set_angle(90) # Start at idle/center position

    # Initialize IoT Client
    cloud = CloudClient(IOT_CONFIG)
    cloud.connect()

    print("Waste Segregation System Started...")

    try:
        while True:
            # 1. Monitoring Bin Level (using single sensor for demonstration)
            current_fill = ultrasonic.get_fill_percentage(THRESHOLDS["BIN_HEIGHT_CM"])
            
            fill_levels = {
                "wet": current_fill, 
                "dry": current_fill,
                "metal": current_fill
            }

            # 2. Detection and Segregation Logic
            if ir_sensor.is_waste_detected():
                print("Waste Detected! Classifying...")
                time.sleep(1) # Wait for sensors to stabilize

                waste_type = "dry" # Default
                
                if metal_sensor.is_metal():
                    waste_type = "metal"
                    servo.set_angle(0) # Move to metal position (-90 relative)
                elif moisture_sensor.is_wet():
                    waste_type = "wet"
                    servo.set_angle(180) # Move to wet position (+90 relative)
                else:
                    servo.set_angle(90) # Move to dry/idle position (0 relative)

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
