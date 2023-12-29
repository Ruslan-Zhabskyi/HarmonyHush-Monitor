from picamera import PiCamera
from sense_hat import SenseHat
import datetime
import storeFileFB
import time

camera = PiCamera()
sense = SenseHat()

camera.start_preview()
frame = 1

while True:
    for event in sense.stick.get_events():
        if event.action == "pressed" and event.direction == "middle":
            fileLoc = f'./images/frame{frame}.jpg'
            currentTime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            camera.capture(fileLoc)
            print(f'frame {frame} taken at {currentTime}')
            storeFileFB.store_file(fileLoc)
            storeFileFB.push_db(fileLoc, currentTime)
            print('Image stored and location pushed to db')

            sense.show_message(f"Frame {frame}", scroll_speed=0.05)
            frame += 1

    time.sleep(0.1)  # Sleep to avoid high CPU usage

