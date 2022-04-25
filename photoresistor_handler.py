from gpiozero import LightSensor
from ADCDevice import *
import firebase_setup
from firebase_admin import firestore
from signal import pause
import constant
import math

adc = ADCDevice()
adc = ADS7830()    
lightVal = None
status = None

db = firestore.client()
collection = firebase_setup.db.collection(constant.COLLECTION_NAME)
doc_lights_ref = collection.document(constant.LIGHT_DATA)
doc_lights_ref.update({u'status':None})
doc_lights_ref.update({u'value':None})

def check_lights():
    global lightVal
    lightVal = adc.analogRead(0)
    print(lightVal)
    doc_lights_ref.update({u'value': lightVal})
    if lightVal <= 65:
        doc_lights_ref.update({u'status': "On"})
    elif lightVal >= 66:
        doc_lights_ref.update({u'status': "Off"})
    else:
        doc_lights_ref.update({u'status': "?"})
