import RPi.GPIO as GPIO
import time
from config import PINS, THRESHOLDS
from sensors.ir_sensor import IRSensor
from sensors.moisture_sensor import MoistureSensor
from sensors.metal_sensor import MetalSensor
from sensors.ultrasonic_sensor import UltrasonicSensor
from actuators.servo_motor import ServoMotor

def test_sensors():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    print("--- Waste Segregation System: Hardware Test Mode ---")
    
    # Initialize Sensors
    ir = IRSensor(PINS["SENSORS"]["IR_DETECTION"])
    moisture = MoistureSensor(PINS["SENSORS"]["MOISTURE_DIGITAL"])
    metal = MetalSensor(PINS["SENSORS"]["METAL_DETECTION"])
    
    # Dual Ultrasonic Initialization
    ultrasonic_wet = UltrasonicSensor(
        PINS["SENSORS"]["ULTRASONIC_WET"]["TRIG"], 
        PINS["SENSORS"]["ULTRASONIC_WET"]["ECHO"]
    )
    ultrasonic_metaldry = UltrasonicSensor(
        PINS["SENSORS"]["ULTRASONIC_METALDRY"]["TRIG"], 
        PINS["SENSORS"]["ULTRASONIC_METALDRY"]["ECHO"]
    )
    
    # Initialize Actuator
    servo = ServoMotor(PINS["ACTUATORS"]["SERVO_MAIN"])

    print("\nSensors initialized. Starting loop...")
    print("Move objects in front of sensors to see real-time status.")

    try:
        while True:
            print("\n" + "="*50)
            
            # 1. Test IR Sensor (Capture fast events)
            ir_val = ir.is_waste_detected()
            print(f"IR Sensor:      {'[ DETECTED ]' if ir_val else '[ CLEAN ]'}")

            # 2. Test Moisture Sensor
            wet_val = moisture.is_wet()
            print(f"Moisture:       {'[ WET ]' if wet_val else '[ DRY ]'}")

            # 3. Test Metal Sensor
            metal_val = metal.is_metal()
            print(f"Metal:          {'[ METAL ]' if metal_val else '[ NO METAL ]'}")

            # 4. Test Dual Ultrasonic
            dist_w = ultrasonic_wet.get_distance()
            fill_w = ultrasonic_wet.get_fill_percentage(THRESHOLDS["BIN_HEIGHT_CM"])
            
            dist_md = ultrasonic_metaldry.get_distance()
            fill_md = ultrasonic_metaldry.get_fill_percentage(THRESHOLDS["BIN_HEIGHT_CM"])
            
            print(f"Wet Bin:        Dist: {dist_w:5.1f}cm | Fill: {fill_w:3.0f}%")
            print(f"Metal/Dry Bin:  Dist: {dist_md:5.1f}cm | Fill: {fill_md:3.0f}%")

            # 5. Test Servo (Show current position)
            print("Servo Motor:    Holding at Center (90 deg)")
            
            print("="*50)
            print("Press Ctrl+C to stop testing.")
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nTest completed. Cleaning up GPIO...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    test_sensors()
