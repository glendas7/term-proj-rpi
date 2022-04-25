import RPi.GPIO as GPIO
import dht11
import firebase_setup
from firebase_admin import firestore
import constant

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin = 26)
result = instance.read()
humidity = None
tempF = None
tempC = None

db = firestore.client()
collection = firebase_setup.db.collection(constant.COLLECTION_NAME)
doc_enviro_ref = collection.document(constant.ENVIRONMENT_DATA)
doc_lcd_ref = collection.document(constant.LCD_DATA)

doc_enviro_ref.update({u'tempC': None})
doc_enviro_ref.update({u'tempF': None})
doc_enviro_ref.update({u'humidity':None})

def check_enviro():
    if result.is_valid():
        global tempC, humidity
        tempC = "%-3.1f C" % result.temperature
        tempF = "%-3.1f F" % ((result.temperature*2)+30)
        humidity = "%-3.1f %%" % result.humidity
        #print("TempC ", tempC, "TempF ", tempF, "Humidity: ", humidity)
        doc_enviro_ref.update({u'tempC': tempC})
        doc_enviro_ref.update({u'tempF': tempF})
        doc_enviro_ref.update({u'humidity': humidity})
        doc_lcd_ref.update({u'message': 'TEMP: ' + tempF +'\n' + 'HUMID: ' + humidity})
    else:
        print("Error: %d" % result.error_code)
