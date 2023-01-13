# Imports go at the top
from microbit import *
from timeutils import *
from app import App
from serial import SerialHandler
from communications import *
from models import Lamp


# set current date and time in datetime object
datetime=DateTime(
    year=2020,
    month=12,
    day=31,
    hours=23,
    minutes=59,
    seconds=55,
)
# set local device its UUID
UUID = "RED"

app = App(UUID, datetime)
# app.lamps.add(Lamp("RED", False))
app.lamps.add(Lamp("GREEN", True))
app.lamps.add(Lamp("BLACK", False))
app.lamps.add(Lamp("YELLOW", False))
app.lamps.add(Lamp("WHITE", False))

serial = SerialHandler(app)
messageHandler = MessageHandler(app)

while True:
    serial.handle()
    messageHandler.handle()
    app.run()
    


    
    
    
        
