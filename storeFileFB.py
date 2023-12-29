import firebase_admin
from firebase_admin import credentials, storage, db
import os

cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'harmonyhushmonitor.appspot.com',
    'databaseURL': 'https://harmonyhushmonitor-default-rtdb.europe-west1.firebasedatabase.app/'
})

bucket = storage.bucket()

ref = db.reference('/')
home_ref = ref.child('file')  # Define home_ref here

def store_file(fileLoc):
    filename = os.path.basename(fileLoc)

    # Store File in FB Bucket
    blob = bucket.blob(filename)
    outfile = fileLoc
    blob.upload_from_filename(outfile)

def push_db(fileLoc, time):
    filename = os.path.basename(fileLoc)

    # Push file reference to image in Realtime DB
    home_ref.push({
        'image': filename,
        'timestamp': time
    })

def push_image(fileLoc, time, frame):
    filename = os.path.basename(fileLoc)

    # Push file reference to image in Realtime DB under 'image'
    image_ref = ref.child('image')
    image_ref.push({
        'file': filename,
        'timestamp': time,
        'frame': frame
    })

def push_sensor_data(fileLoc, time, frame):
    filename = os.path.basename(fileLoc)

    # Push file reference to data in Realtime DB under 'data'
    data_ref = ref.child('data')
    data_ref.push({
        'file': filename,
        'timestamp': time,
        'frame': frame
    })

