from gpiozero import Servo
from ADCDevice import *
import firebase_setup
from firebase_admin import firestore
from gpiozero.pins.pigpio import PiGPIOFactory
import constant

db = firestore.client()
collection = firebase_setup.db.collection(constant.COLLECTION_NAME)
doc_buttons_ref = collection.document(constant.BUTTON_DATA)
doc_joystick_ref = collection.document(constant.JOYSTICK_DATA)
doc_joystick_ref.update({u'xVal': 0})

def on_buttonsdoc_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        arrowVal = doc.to_dict()["arrowVal"]
        if arrowVal == 0:
            servo.mid()
        elif arrowVal == 1:
            servo.max()
        elif arrowVal == -1:
            servo.min()

doc_buttons_watch = doc_buttons_ref.on_snapshot(on_buttonsdoc_snapshot)

factory = PiGPIOFactory()
joystick = ADCDevice()
joystick = ADS7830()
servo = Servo(18, pin_factory=factory)
servo.mid()


def update():
    xVal= joystick.analogRead(6)
    yVal= joystick.analogRead(7)
    print("xVal: ", xVal)
    if xVal == 0:
        servo.min()
    elif xVal > 0 and xVal < 110:
       servo.value = -.5
    elif xVal >= 110 and xVal <= 145:
        servo.mid()
    elif xVal >= 240:
        servo.max()
    elif xVal > 145 and xVal < 240:
        servo.value = .5
    doc_joystick_ref.update({u'xVal': xVal})