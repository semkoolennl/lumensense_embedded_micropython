# Imports go at the top
from microbit import *
from timeutils import *
from communications import *
from models import *
from controllers import *

# set local device its UUID
UUID = "0B01"
# set current date and time in datetime object
datetime=DateTime(
    year=2020,
    month=12,
    day=31,
    hours=23,
    minutes=59,
    seconds=55,
)

# initiate clock for keeping track of date and time
clock = Clock(datetime)
# initiate countdown timer object
timer  = Timer()
logger = Logger(clock)


# creates a lamp entity for this device
lamp = Lamp(UUID)

# initiate collection object for lamps and set local lamp
collection = LampCollection(lamp)

# initiate message handler and pass the lamp collection
motionHandler  = MotionHandler(timer, collection)
messageHandler = MessageHandler(collection, logger)
lightHandler   = LightHandler(timer)


start = False

# main loop
while True:       
    clock.tick()
    timer.update(clock.lastTick)

    messageHandler.handle()
    motionHandler.handle()
    lightHandler.handle()
    print(logger.clock.datetime)
    
    
        
