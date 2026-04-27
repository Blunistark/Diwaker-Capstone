"""
Configuration settings for the Waste Segregation Monitoring System.
Includes GPIO pin mappings and IoT parameters.
"""

# GPIO Pin Mappings (BCM Mode)
PINS = {
    "SENSORS": {
        "IR_DETECTION": 17,       # IR Sensor for waste detection
        "MOISTURE_DIGITAL": 27,   # Moisture Sensor digital output
        "METAL_DETECTION": 22,    # Metal Sensor
        "ULTRASONIC": {           # Single Ultrasonic Sensor
            "TRIG": 23,
            "ECHO": 24
        }
    },
    "ACTUATORS": {
        "SERVO_MAIN": 18          # Single Servo for directing waste
    }
}

# IoT / Cloud Settings
IOT_CONFIG = {
    "BROKER": "broker.hivemq.com",
    "PORT": 1883,
    "TOPIC_PREFIX": "waste_monitoring/presidency_univ/",
    "CLIENT_ID": "raspberry_pi_segregator_001"
}

# System Thresholds
THRESHOLDS = {
    "FILL_LEVEL_CRITICAL": 90,    # Percentage
    "BIN_HEIGHT_CM": 30           # Height of your bin in cm
}
