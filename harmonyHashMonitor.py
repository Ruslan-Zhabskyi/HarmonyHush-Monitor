import subprocess
import time
from threading import Thread
from queue import Queue
import datetime
from sense_hat import SenseHat
import logging
from dotenv import dotenv_values
import storeFileFB
import paho.mqtt.client as mqtt
from urllib.parse import urlparse

sense = SenseHat()
sense.clear()

output_queue = Queue()

# Function to start udpMotionListner.py in a subprocess
def start_listener(queue):
    listener_process = subprocess.Popen(['python', 'udpMotionListner.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    while listener_process.poll() is None:
        try:
            udp_output = listener_process.stdout.readline().strip()

            if udp_output and "movement detected" in udp_output.lower():
                queue.put("Movement Detected")
        except Exception as e:
            print(f"Error: {e}")
            break

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

# Function to configure MQTT client
def configure_mqtt():
    config = dotenv_values(".env")
    logging.basicConfig(level=logging.INFO)

    mqttc = mqtt.Client(client_id=config["clientId"])
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish

    mqttc.username_pw_set(config["username"], config["password"])

    url_str = config["mqttUrl"]
    url = urlparse(url_str)
    base_topic = url.path[1:]

    mqttc.connect(url.hostname, url.port)
    mqttc.loop_start()

    topic = "channels/" + config["channelId"] + "/publish"

    return mqttc, topic, config

# Define event callbacks for MQTT
def on_connect(client, userdata, flags, rc):
    logging.info("Connection Result: " + str(rc))

def on_publish(client, obj, mid):
    logging.info("Message Sent ID: " + str(mid))

# Start the listener thread
listener_thread = Thread(target=start_listener, args=(output_queue,), daemon=True)
listener_thread.start()

# Get MQTT client, topic, and config
mqtt_client, mqtt_topic, config = configure_mqtt()

# Initialize the frame variable
frame = 1

while True:
    try:
        if not output_queue.empty():
            udp_output = output_queue.get()
            file_loc = f'./images/frame50.jpeg'
            current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # Assume the storeFileFB handles the image capture process
            # and use it to upload the frame21.png image
            storeFileFB.store_file('./images/frame50.jpeg')
            storeFileFB.push_db(file_loc, current_time)
            print('Image stored and location pushed to db')

            frame += 1

        ambient_temp = get_raspberry_pi_temperature()

        temp = round(sense.get_temperature() - (ambient_temp - sense.get_temperature()), 2)
        humidity = round(sense.get_humidity(), 2)
        payload = "field1=" + str(temp) + "&field2=" + str(humidity)
        mqtt_client.publish(mqtt_topic, payload)
        time.sleep(int(config["transmissionInterval"]))

    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.1)


