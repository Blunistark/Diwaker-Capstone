import paho.mqtt.client as mqtt
import json
import time

class CloudClient:
    """
    Handles communication with the cloud dashboard via MQTT.
    """
    def __init__(self, config):
        self.config = config
        self.client = mqtt.Client(self.config["CLIENT_ID"])
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

    def connect(self):
        try:
            self.client.connect(self.config["BROKER"], self.config["PORT"], 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"Failed to connect to cloud: {e}")
            return False

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker successfully")
        else:
            print(f"Connection failed with code {rc}")

    def on_publish(self, client, userdata, mid):
        print(f"Data published successfully (mid: {mid})")

    def publish_status(self, bin_levels, waste_type_detected):
        """
        Publishes real-time status to the dashboard.
        """
        payload = {
            "timestamp": time.time(),
            "bin_levels": bin_levels,
            "last_waste_type": waste_type_detected,
            "system_status": "Active"
        }
        topic = self.config["TOPIC_PREFIX"] + "status"
        self.client.publish(topic, json.dumps(payload))

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
