# Setting up: HarmonyHush-Monitor 
Computer Systems &amp; Networks assignment 2

<p>HarmonyHush is equipped with sensors and a camera to monitor the environment. It uses Machine Learning to analyse the environment around the child during sleep time.</p>

## Set up sense Hat and Camera
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

## Set up Firebase Storrage

- Install the Firebase Admin package on Raspberry Pi (rpi)
```
pip install firebase-admin==5.4.0
```
- Register app with Firebase [link](https://firebase.google.com/docs/web/setup)
- Create a copy the serviceAccountKey.json in the project directory on rpi
- create [storeFileFB.py](https://github.com/Ruslan-Zhabskyi/HarmonyHush-Monitor/blob/main/storeFileFB.py) in the directory
Note: In storeFileFB.py, replace the value for storageBucket and databaseURL




