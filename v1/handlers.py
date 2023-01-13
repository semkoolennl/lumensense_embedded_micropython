from communications import RTTP
from models import *
from logger import Logger
from serial import *
from timeutils import Timer
from microbit import *

class Handler:
    def __init__(self, lamps: LampCollection, logger: Logger):
        self.lamps      = lamps
        self.rttp       = RTTP(lamps.local.uuid, logger)
        self.logger     = logger

    def activate(self):
        self.logger.general("MotionHandler - Motion detected, activating")
        self.rttp.setMessage("ACT")
        self.lamps.local.activated = True
        self.rttp.send()

    def deactivate(self):
        self.logger.general("MotionHandler - No motion detected, deactivating")
        self.rttp.setMessage("DEACT")
        self.lamps.local.activated = False
        self.rttp.send()


        
class MotionHandler(Handler):
    def __init__(self, lamps: LampCollection, logger: Logger):
        super().__init__(lamps, logger)
        self.previous   = False
        self.resetTimer = False
        

    def handle(self):
        motion = pin1.read_analog() > 500    
        #print(pin1.read_analog())
        #print(str(motion) + " - " + str(self.previous))
        if self.previous == motion:
            if self.lamps.isActivated():
                self.resetTimer = True
            else:
                self.resetTimer = False
                self.lamps.local.iactivated = False
        else:
            self.previous = motion
            if motion:
                self.logger.general("MotionHandler - Motion detected, activating")
                self.activate()
            else:
                self.logger.general("MotionHandler - No motion detected, deactivating")
                self.deactivate()


class LightHandler(Handler):
    def __init__(self, lamps: LampCollection, logger: Logger):
        super().__init__(lamps, logger)
        self.lightOn = False

    def handle(self, timer):
        if timer.time > 0 and not self.lightOn:
            self.logger.general("LightHandler - Light turned on")
            self.lightOn = True
            pin0.write_digital(1)
            display.show(Image.HEART)
        elif timer.time <= 0 and self.lightOn:
            self.logger.general("LightHandler - Light turned off")
            self.lightOn = False
            self.deactivate()
            pin0.write_digital(0)
            display.clear()

        
        
            
            
            
        