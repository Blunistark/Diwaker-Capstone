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
    
    # Initialize
    ir = IRSensor(PINS["SENSORS"]["IR_DETECTION"])
    moisture = MoistureSensor(PINS["SENSORS"]["MOISTURE_DIGITAL"])
    metal = MetalSensor(PINS["SENSORS"]["METAL_DETECTION"])
    ultrasonic = UltrasonicSensor(PINS["SENSORS"]["ULTRASONIC"]["TRIG"], PINS["SENSORS"]["ULTRASONIC"]["ECHO"])
    servo = ServoMotor(PINS["ACTUATORS"]["SERVO_MAIN"])

    try:
        while True:
            print("\n" + "="*40)
            
            # 1. Test IR Sensor
            ir_val = ir.is_waste_detected()
            print(f"IR Sensor:      {'[ DETECTED ]' if ir_val else '[ CLEAN ]'}")

            # 2. Test Moisture Sensor
            wet_val = moisture.is_wet()
            print(f"Moisture Sensor: {'[ WET ]' if wet_val else '[ DRY ]'}")

            # 3. Test Metal Sensor
            metal_val = metal.is_metal()
            print(f"Metal Sensor:    {'[ METAL ]' if metal_val else '[ NO METAL ]'}")

            # 4. Test Ultrasonic
            dist = ultrasonic.get_distance()
            fill = ultrasonic.get_fill_percentage(THRESHOLDS["BIN_HEIGHT_CM"])
            print(f"Ultrasonic:     Distance: {dist:.1f}cm | Fill: {fill}%")

            # 5. Test Servo (Hold any key to sweep, or just show idle)
            print("Servo Motor:    Idle (90 deg)")
            
            print("="*40)
            print("Press Ctrl+C to stop testing.")
            
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nTest completed. Cleaning up GPIO...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    test_sensors()
