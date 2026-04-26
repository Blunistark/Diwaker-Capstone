# Waste Segregation Monitoring System for Urban Local Bodies

This project implements an automated waste segregation and monitoring system using Raspberry Pi and IoT technology. It classifies waste into **Wet**, **Dry**, and **Metal** categories and provides real-time monitoring of bin fill levels via a cloud dashboard.

## Features

- **Automated Classification**: Uses IR, Moisture, and Metal sensors to identify waste types.
- **Smart Segregation**: Controls servo motors to direct waste into the correct bin.
- **Real-time Monitoring**: Uses Ultrasonic sensors to track bin levels and publishes data to a cloud dashboard (MQTT).
- **Urban Scalability**: Designed for deployment in smart city environments.

## Project Structure

- `main.py`: Main orchestration script.
- `config.py`: GPIO pin and IoT configurations.
- `sensors/`:
    - `ir_sensor.py`: Waste presence detection.
    - `moisture_sensor.py`: Wet/Dry classification.
    - `metal_sensor.py`: Metallic waste detection.
    - `ultrasonic_sensor.py`: Bin level monitoring.
- `actuators/`:
    - `servo_motor.py`: Waste redirection control.
- `iot/`:
    - `cloud_client.py`: MQTT communication for remote monitoring.

## Installation

1. Clone the repository to your Raspberry Pi.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update `config.py` with your specific GPIO pin mappings.
4. Run the system:
   ```bash
   python main.py
   ```

## Hardware Requirements

- Raspberry Pi (3/4/Zero)
- IR Obstacle Sensor
- Soil Moisture Sensor
- Inductive Proximity Sensor (Metal detection)
- HC-SR04 Ultrasonic Sensors (x3)
- MG995/SG90 Servo Motor
- Connecting Wires & Breadboard

## Contributors

- **Diwakar Reddy A** - Presidency University, Bengaluru
- **Guide**: Mr. Anandan B

