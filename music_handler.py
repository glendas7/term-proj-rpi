import pygame
import firebase_setup
from firebase_admin import firestore
import constant

db = firestore.client()
collection = firebase_setup.db.collection(constant.COLLECTION_NAME)
doc_buttons_ref = collection.document(constant.BUTTON_DATA)

doc_buttons_ref.update({u'musicButton': False})
btn = False

pygame.mixer.init()
sound1 = pygame.mixer.Sound("nature.ogg")
sound2 = pygame.mixer.Sound("water.ogg")

def water_plants():
    print("click")
    pygame.mixer.find_channel().play(sound2)
    doc_buttons_ref.update({u'waterButton': False})
    
def start_music():
    pygame.mixer.find_channel().play(sound1)
    pygame.mixer.music.play()
    
def stop_music():
    pygame.mixer.music.stop()

def on_buttonsdoc_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        global btn
        musicBtn = doc.to_dict()["musicButton"]
        waterBtn = doc.to_dict()["waterButton"]
        if waterBtn == True:
            water_plants()
        if musicBtn == True:
            start_music()
        elif musicBtn == False:
            stop_music()
            
doc_buttons_watch = doc_buttons_ref.on_snapshot(on_buttonsdoc_snapshot)

