from communications import RTTP
from models import Lamp, LampCollection, Message
from logger import Logger
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
            self.logger.general("MotionHandler - Motion state change")
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

        

class MessageHandler(Handler):
    def __init__(self, lamps: LampCollection, logger: Logger):
        super().__init__(lamps, logger)

    def handle(self):
        while (self.rttp.nextMessage()):
            message = self.rttp.message
            if message.recipient != "ALL" and message.recipient != self.lamps.local.uuid:
                continue
                   
            if message.method == "ACT":
                self.handleACT(message)
            elif message.method == "IACT":
                self.handleIACT(message)
            elif message.method == "DEACT":
                self.handleDEACT(message)
            elif message.method == "GET":
                self.handleGET(message)
            elif message.method == "POST":
                self.handlePOST(message)
            else:
                self.handleUnknownMethod(message)


    def handleACT(self, message: Message):
        self.logger.general("MessageHandler - handleACT()")
        sourceLamp = self.lamps.getById(message.source)
        sourceLamp.activated = True
        self.lamps.set(sourceLamp)
        if sourceLamp.activator:
            self.lamps.local.iactivated = True
        self.rttp.setMessage("IACT")
        self.rttp.send()

    def handleIACT(self, message: Message):
        self.logger.general("MessageHandler - handleIACT()")
        sourceLamp = self.lamps.getById(message.source)
        sourceLamp.iactivated = True

    def handleDEACT(self, message: Message):
        self.logger.general("MessageHandler - handleDEACT()")
        sourceLamp = self.lamps.getById(message.source)
        if sourceLamp.activated:
            sourceLamp.activated = False
            sourceLamp.activations.direct += 1
            self.lamps.local.activations.indirect += 1
        if self.lamps.local.iactivated:
            self.lamps.local.iactivated = False
            self.lamps.local.activations.indirect += 1
        self.lamps.set(sourceLamp)

    def handleGET(self, message):
        self.logger.general("MessageHandler - handleGET()")
        print(message.encode())

    def handlePOST(self, message):
        self.logger.general("MessageHandler - handlePOST()")
        print(message.encode())

    def handleUnknownMethod(self, message: Message):
        self.logger.general("MessageHandler - handleUnknownMethod()")
        msg = "'" + message.encode() + "'"
        self.logger.error("Unkown method: " + msg, "fatal")