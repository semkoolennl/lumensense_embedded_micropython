from models import *
from serial import *
from microbit import *

class Handler:
    def __init__(self, app):
        self.app = app

    def activate(self):
        self.app.rttp.setMessage("ACT")
        self.app.lamps.local.activated = True
        self.app.lamps.local.activations += 1
        self.app.rttp.send()

    def deactivate(self, timer):
        if timer:
            self.app.rttp.setMessage("DEACT")
        self.app.lamps.local.activated = False
        self.app.rttp.send()


        
class MotionHandler(Handler):
    def __init__(self, app):
        super().__init__(app)
        self.previous   = False
        self.resetTimer = False
        

    def handle(self):
        analog = pin1.read_analog()
        motion = analog > 800    
        if self.previous == motion:
            if self.app.lamps.isActivated():
                self.resetTimer = True
            else:
                self.resetTimer = False
                self.app.lamps.local.iactivated = False
        else:
            self.previous = motion
            if motion:
                self.app.logger.general("MotionHandler - Motion detected, activating")
                self.activate()
            else:
                self.app.logger.general("MotionHandler - No motion detected, deactivating")
                self.deactivate(False)
           

class LightHandler(Handler):
    def __init__(self, app):
        super().__init__(app)
        self.lightOn = False

    def handle(self):
        if self.app.timer.time > 0 and not self.lightOn:
            self.lightOn = True
            pin0.write_digital(1)
            display.show(Image.HEART)
            self.app.lamps.local.lighton = True
        elif self.app.timer.time <= 0 and self.lightOn:
            self.lightOn = False
            self.deactivate(True)
            pin0.write_digital(0)
            display.clear()
            self.app.lamps.local.lighton = False
   