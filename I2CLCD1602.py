from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import firebase_setup
from firebase_admin import firestore
import constant

db = firestore.client()
collection = firebase_setup.db.collection(constant.COLLECTION_NAME)
doc_lcd_ref = collection.document(constant.LCD_DATA)
doc_lcd_ref.update({u'message': None})

def on_lcd_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        message = doc.to_dict()["message"]
        if message:
            loop(message)
            
doc_lcd_watch = doc_lcd_ref.on_snapshot(on_lcd_snapshot)

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

def loop(msg):
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    while(True):         
        #lcd.clear()
        lcd.setCursor(0,0)  # set cursor position
        lcd.message(msg)# display CPU temperature
        
def destroy():
    lcd.clear()
