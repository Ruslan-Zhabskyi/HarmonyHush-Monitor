import subprocess
import time
from threading import Thread
from queue import Queue
from picamera import PiCamera
from sense_hat import SenseHat
import datetime
import json
import storeFileFB

camera = PiCamera()
sense = SenseHat()

camera.start_preview()
frame = 1

# Function to start udpMotionListner.py in a subprocess
def start_listener(queue):
    listener_process = subprocess.Popen(['python', 'udpMotionListner.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    while listener_process.poll() is None:  # Check if the subprocess is still running
        try:
            # Attempt to read from the subprocess stdout
            udp_output = listener_process.stdout.readline().strip()

            # Check if "Movement Detected" is present in the output (case insensitive)
            if udp_output and "movement detected" in udp_output.lower():
                queue.put("Movement Detected")
        except Exception as e:
            # Print the exception for debugging
            print(f"Error: {e}")
            break

# Function to capture image and update temperature and humidity data
def capture_and_update(queue, frame):
    try:
        while True:
            # Capture image only when motion is detected
            if not queue.empty():
                # Process the "Movement Detected" message
                udp_output = queue.get()

                # Capture image
                file_loc = f'./images/frame{frame}.jpg'
                camera.capture(file_loc)
                print(f'Frame {frame} taken')
                storeFileFB.store_file(file_loc)
                storeFileFB.push_db(file_loc, f"Image from Frame {frame}")
                frame += 1
            # Record temperature and humidity
            temperature = sense.get_temperature()
            humidity = sense.get_humidity()

            # Save sensor data to JSON file
            sensor_data = {
                "timestamp": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "temperature": temperature,
                "humidity": humidity
            }

            with open('./sensor_data/all_data.json', 'a') as json_file:
                json.dump(sensor_data, json_file)
                json_file.write('\n')  # Add newline between entries

            storeFileFB.push_db('./sensor_data/all_data.json', "Sensor data updated")

            time.sleep(30)  # Sleep for 30 seconds between captures

    except KeyboardInterrupt:
        print("Exiting...")

# Create a queue for inter-thread communication
output_queue = Queue()

# Start the listener thread
listener_thread = Thread(target=start_listener, args=(output_queue,), daemon=True)
listener_thread.start()

# Start the capture and update thread
capture_thread = Thread(target=capture_and_update, args=(output_queue, frame), daemon=True)
capture_thread.start()

# Wait for threads to finish
listener_thread.join()
capture_thread.join()
