import paho.mqtt.client as mqtt
import time
import json
from track import start_tracking

class Mqtt_Class:
    def __init__(self, client_id):
        print("initializing class")
        self.broker_address="localhost"
        self.client_id = client_id
        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address, port=1883)

    def on_message(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)
        if message.topic == "track":
            tracked_info = start_tracking(str(message.payload.decode("utf-8")))
            if tracked_info:
                self.publish_topic("tracked", tracked_info)
                print("tracked")
            else:
                print("Error, Failed to track")

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("connected to mqtt broker Returned code=",rc)
        else:
            print("Bad connection Returned code=",rc)

    def subscribe_topic(self, topic):
        print("Subscribing to topic ",topic)
        self.client.subscribe(topic)

    def publish_topic(self, topic, payload):
        print("Publishing message to topic ",topic)
        self.client.publish(topic,payload)

