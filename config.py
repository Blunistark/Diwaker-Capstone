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
        "ULTRASONIC_WET": {
            "TRIG": 23,
            "ECHO": 24
        },
        "ULTRASONIC_DRY": {
            "TRIG": 25,
            "ECHO": 8
        },
        "ULTRASONIC_METAL": {
            "TRIG": 7,
            "ECHO": 1
        }
    },
    "ACTUATORS": {
        "SERVO_MAIN": 18,         # Main servo for directing waste
        "SERVO_SECONDARY": 12     # Secondary servo if needed
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
    "MOISTURE_LEVEL_WET": 500     # Analog value if using ADC
}
