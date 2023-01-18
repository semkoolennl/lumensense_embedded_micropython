# Imports go at the top
from microbit import *
from timeutils import *
from app import App
from serial import SerialHandler
from communications import *
from models import Lamp
from handlers import *


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
UUID = "BLACK"

app = App(UUID, datetime)
# app.lamps.add(Lamp("BLACK", False))
app.lamps.add(Lamp("YELLOW", True))
app.lamps.add(Lamp("RED", False))
app.lamps.add(Lamp("GREEN", False))

serialHandler  = SerialHandler(app)
messageHandler = MessageHandler(app)
motionHandler  = MotionHandler(app)
lightHandler   = LightHandler(app)

while True:
    try:
        serialHandler.handle()
        messageHandler.handle()
        motionHandler.handle()
        
        if motionHandler.resetTimer:
            app.timer.time = 3000
            
        lightHandler.handle()
    except Exception as e:
        app.logger.error("Unknown error handlers: " + str(e))
        sleep(5000)

    try:
        app.run()
    except Exception as e:
        app.logger.error("Unknown erro app.run(): " + str(e))
        sleep(5000)
