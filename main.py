from gpiozero import Servo
from time import sleep
from ADCDevice import *
import firebase_setup
from firebase_admin import firestore
import camera_handler
import constant

db = firestore.client()
collection = firebase_setup.db.collection(constant.COLLECTION_NAME)
doc_joystick_ref = collection.document(constant.JOYSTICK_DATA)
doc_buttons_ref = collection.document(constant.BUTTON_DATA)
doc_camera_ref = collection.document(constant.CAMERA_DATA)

doc_joystick_ref.update({u'xVal': 0})
doc_camera_ref.update({u'url':None})
doc_camera_ref.update({u'timestamp':None})
doc_buttons_ref = collection.document(constant.BUTTON_DATA)
doc_camera_ref = collection.document(constant.CAMERA_DATA)
doc_buttons_ref.update({u'picButton':False})

def on_buttonsdoc_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        global permission_status
        picture_button_status = doc.to_dict()["picButton"]
        if picture_button_status:
            print('updated pic url')
            camera_handler.capture('1.jpg')
            doc_buttons_ref.update({u'picButton':False})
            

doc_buttons_ref = collection.document(constant.BUTTON_DATA)
doc_buttons_watch = doc_buttons_ref.on_snapshot(on_buttonsdoc_snapshot)

joystick = ADCDevice()
joystick = ADS7830()

s  = 18
servo = Servo(s)
servo.mid()

while True:
    xVal= joystick.analogRead(6)
    yVal= joystick.analogRead(7)
    print("xVal: ", xVal)
    if xVal == 0:
        servo.min()
    else:
        servo.max()
        
    doc_joystick_ref.update({u'xVal': xVal})
