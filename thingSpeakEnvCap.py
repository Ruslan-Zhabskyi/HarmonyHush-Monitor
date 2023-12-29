#!/usr/bin/python3

import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import sys
import time
from sense_hat import SenseHat
import logging
from dotenv import dotenv_values
import psutil

# Function to get the ambient temperature of the Raspberry Pi
def get_raspberry_pi_temperature():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as file:
            temperature_str = file.readline().strip()
            cpu_temp = float(temperature_str) / 1000.0
        return cpu_temp
    except Exception as e:
        logging.error('Failed to get Raspberry Pi temperature: {}'.format(e))
        return 0

# Initialise SenseHAT
sense = SenseHat()
sense.clear()

# Load MQTT configuration values from .env file
config = dotenv_values(".env")

# Configure Logging
logging.basicConfig(level=logging.INFO)

# Define event callbacks for MQTT
def on_connect(client, userdata, flags, rc):
    logging.info("Connection Result: " + str(rc))

def on_publish(client, obj, mid):
    logging.info("Message Sent ID: " + str(mid))

mqttc = mqtt.Client(client_id=config["clientId"])

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# Parse MQTT URL for connection details
url_str = sys.argv[1]
print(url_str)
url = urlparse(url_str)
base_topic = url.path[1:]

# Configure MQTT client with user name and password
mqttc.username_pw_set(config["username"], config["password"])

# Connect to MQTT Broker
mqttc.connect(url.hostname, url.port)
mqttc.loop_start()

# Set Thingspeak Channel to publish to
topic = "channels/"+config["channelId"]+"/publish"

# Publish a message to temp every 15 seconds
while True:
    try:
        ambient_temp = get_raspberry_pi_temperature()

        temp = round(sense.get_temperature() - (ambient_temp - sense.get_temperature()), 2)
        humidity = round(sense.get_humidity(), 2)
        payload = "field1=" + str(temp) + "&field2=" + str(humidity)
        mqttc.publish(topic, payload)
        time.sleep(int(config["transmissionInterval"]))
    except Exception as e:
        logging.error('Exception: {}'.format(e))

