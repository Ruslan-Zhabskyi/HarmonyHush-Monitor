# Setting up: HarmonyHush-Monitor 
Computer Systems &amp; Networks assignment 2

<p>HarmonyHush is equipped with sensors and a camera to monitor the environment. It uses Machine Learning to analyse the environment around the child during sleep time.</p>

## Equipment needed
- Raspberry Pi 4 Model B
- Sense HAT
- Camera

## Technologies:
- Python
- JavaScript
- TensorFlow
- Cisco Packet Tracer
- ThingSpeak IoT platform
- MQTT, IFTTT
- HTML, CSS
- Glitch, GitHub

## 1. Set up sense Hat and Camera
### Make sure your system is up to date 
```
sudo apt update
sudo apt upgrade
```

### Enablle camera:
```
sudo raspi-config

sudo apt install sense-hat
sudo apt install python3-pil
```
### Enable I2C Interface:
```
sudo raspi-config

sudo raspi-config
```

## 2. Set up Firebase Storrage

- Install the Firebase Admin package on Raspberry Pi (rpi)
```
pip install firebase-admin==5.4.0
```
- Register app with Firebase [link](https://firebase.google.com/docs/web/setup)
- Create a copy the serviceAccountKey.json in the project directory on rpi
- create [storeFileFB.py](https://github.com/Ruslan-Zhabskyi/HarmonyHush-Monitor/blob/main/storeFileFB.py) in the directory
Note: In storeFileFB.py, replace the value for storageBucket and databaseURL

## 3. [Import Cisco Packet Tracer](https://github.com/Ruslan-Zhabskyi/HarmonyHush-Monitor/blob/main/motion_detector.pkt) to replace physical motion sensor
Ensure to update var dstIP in the MCU0 with rpi IP (ifconfig)

## 4. Modify project directory
- Add [Montion Listner python code](https://github.com/Ruslan-Zhabskyi/HarmonyHush-Monitor/blob/main/udpMotionListner.py) to the directoty
- Set up "images" and "sensor_data" directories
```
mkdir images
mkdir sensor_data
```
- Add [originalHarmonyHashMonitor.py](https://github.com/Ruslan-Zhabskyi/HarmonyHush-Monitor/blob/main/originalHarmonyHashMonitor.py) file to the directory

## 5. Set up [ThingSpeak Account](https://thingspeak.com/)
- Create channel with temperature and humidity fields
- Create a ThingSpeak MQTT Device
- Create .env file with configuration data
  ```
  username = [YOUR USER NAME]
  clientId = [YOUR CLIENT ID]
  password = [YOUR PASSWORD]
  mqttUrl = [YOUR MQTT URL]
  channelId = [YOUR CHANNEL ID]
  transmissionInterval = 15
  ```
 ## 6. Set up [IFTT account](https://ifttt.com/explore)
  ##### a. Create an IFTTT account
  ##### b. Create Trigger. Select the Webhooks service, search for "Webhooks," and choose the "Receive a web request" card.
  ##### c. Create Action. Click on "Add" in the "Then That" card. Search for "Email" and select the "Send me an email" card. Connect your email address, update the subject and body of the event email, and click "Continue" and then "Finish."
  ##### d. Get Trigger URL. Click your user icon, go to "Services," scroll down, select "Webhooks," and click on "Documentation."

## 7. ThingHTTP Setup:

### a. Open SensePi Channel in ThingSpeak:
- Go to your SensePi channel in ThingSpeak.

### b. Create ThingHTTP:
- Choose "Apps" => "ThingHTTP" and select "New ThingHTTP."
- Enter the URL from the Webhooks documentation in the "URL" field.
- Set the method to "GET."

## 8. React App Setup:

### a. Create React App:
- In ThingSpeak, go to your channel, choose "Apps" => "React," and click "New React."
- Configure the React app to trigger when temperature is above 22 degrees

### b. Receive Email Notification:
- Once the temperature condition is met, you'll receive an email. This notification occurs only the first time the condition is met.

These steps integrate SensePi, ThingHTTP, and IFTTT to trigger an email notification when the temperature exceeds a specified threshold. Adjust the temperature threshold and other parameters as needed.

```
 


