import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("./serviceAccountKey.json")

## change storageBucket according to your Firebase project
firebase_admin.initialize_app(cred, {
    "storageBucket": "cmsc-4313-iot.appspot.com"
})

## Firestore and Cloud Storage access
db = firestore.client()
bucket = storage.bucket()
