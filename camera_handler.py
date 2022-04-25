from picamera import PiCamera
import time
from datetime import timedelta
import constant
import firebase_setup
from firebase_admin import firestore

camera = PiCamera()
db = firestore.client()
collection = firebase_setup.db.collection(constant.COLLECTION_NAME)
doc_camera_ref = collection.document(constant.CAMERA_DATA)
doc_camera_ref.update({u'url':None})
doc_camera_ref.update({u'timestamp':None})

def capture(name):
    camera.capture(name)
    imageUploadPath = constant.STORAGE_FOLDER_CAMERA_IMAGES + '/' + name
    blob = firebase_setup.bucket.blob(imageUploadPath)
    url = blob.generate_signed_url(expiration=timedelta(days=30),
                                   method="GET")
    blob.upload_from_filename(name)

    doc_camera_ref.update({
        'url': url,
        'timestamp': time.time_ns() # ns since Epoch (Jan 1, 1970)
    })