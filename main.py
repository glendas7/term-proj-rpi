from time import sleep
from ADCDevice import *
import firebase_setup
from gpiozero import Button
from firebase_admin import firestore
import camera_handler
import constant
import dht11_handler
import photoresistor_handler
import I2CLCD1602
import music_handler
import servo_handler

db = firestore.client()
collection = firebase_setup.db.collection(constant.COLLECTION_NAME)
doc_buttons_ref = collection.document(constant.BUTTON_DATA)
doc_buttons_ref.update({u'picButton':False})
doc_buttons_ref.update({u'arrowButton':False})
doc_buttons_ref.update({u'musicButton':False})
arrowBtn = False
waterBtn = Button(5)

def on_buttonsdoc_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        global permission_status
        picture_button_status = doc.to_dict()["picButton"]
        arrow_button_status = doc.to_dict()["arrowButton"]
        global arrowBtn
        if arrow_button_status:
            arrowBtn = True
        else:
            arrowBtn = False
        if picture_button_status:
            print('updated pic url')
            camera_handler.capture('1.jpg')
            doc_buttons_ref.update({u'picButton':False})

doc_buttons_watch = doc_buttons_ref.on_snapshot(on_buttonsdoc_snapshot)

def updateBtn():
    doc_buttons_ref.update({u'waterButton': True})
    
waterBtn.when_pressed = updateBtn
    
while True:
    dht11_handler.check_enviro()
    photoresistor_handler.check_lights()
    if arrowBtn == False:
        servo_handler.update()
    

        
        
