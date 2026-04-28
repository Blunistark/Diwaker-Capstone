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
    
    # Initialize dual ultrasonic sensors for level monitoring
    ultrasonic_wet = UltrasonicSensor(PINS["SENSORS"]["ULTRASONIC_WET"]["TRIG"], PINS["SENSORS"]["ULTRASONIC_WET"]["ECHO"])
    ultrasonic_metaldry = UltrasonicSensor(PINS["SENSORS"]["ULTRASONIC_METALDRY"]["TRIG"], PINS["SENSORS"]["ULTRASONIC_METALDRY"]["ECHO"])

    # Initialize Actuator
    servo = ServoMotor(PINS["ACTUATORS"]["SERVO_MAIN"])
    servo.set_angle(90) # Start at idle/center position

    # Initialize IoT Client
    cloud = CloudClient(IOT_CONFIG)
    cloud.connect()

    print("Waste Segregation System Started...")

    try:
        while True:
            # 1. Monitoring Bin Levels independently
            wet_fill = ultrasonic_wet.get_fill_percentage(THRESHOLDS["BIN_HEIGHT_CM"])
            metaldry_fill = ultrasonic_metaldry.get_fill_percentage(THRESHOLDS["BIN_HEIGHT_CM"])
            
            fill_levels = {
                "wet": wet_fill, 
                "metal_dry": metaldry_fill
            }

            # 2. Detection and Segregation Logic
            if ir_sensor.is_waste_detected():
                print("Waste Detected! Classifying...")
                # Notify dashboard immediately
                cloud.publish_status(fill_levels, "detecting")
                time.sleep(1) # Wait for sensors to stabilize

                waste_type = "dry" # Default
                
                if moisture_sensor.is_wet():
                    waste_type = "wet"
                    servo.set_angle(180) # Move to wet position (+90 relative)
                else:
                    # Anything else (Metal or Dry) goes to the other bin
                    waste_type = "metal_dry"
                    servo.set_angle(0) # Move to metal/dry position (-90 relative)

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
