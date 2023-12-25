import subprocess
import time
from threading import Thread
from queue import Queue
from picamera import PiCamera
import datetime
import storeFileFB

camera = PiCamera()

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

# Create a queue for inter-thread communication
output_queue = Queue()

# Start the listener thread
listener_thread = Thread(target=start_listener, args=(output_queue,), daemon=True)
listener_thread.start()

while True:
    try:
        # Check if "Movement Detected" is present in the queue
        if not output_queue.empty():
            # Process the "Movement Detected" message
            udp_output = output_queue.get()
            file_loc = f'./images/frame{frame}.jpg'
            current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            camera.capture(file_loc)
            print(f'Frame {frame} taken at {current_time}')
            storeFileFB.store_file(file_loc)
            storeFileFB.push_db(file_loc, current_time)
            print('Image stored and location pushed to db')

            frame += 1

    except KeyboardInterrupt:
        print("Exiting...")
        break

    time.sleep(0.1)  # Sleep to avoid high CPU usage

