from communications import RTTP
from models import Lamp, LampCollection, Message
from logger import Logger
from timeutils import Timer
from microbit import *


class MotionHandler:
    def __init__(self, timer: Timer, lamps: LampCollection):
        self.lamps    = lamps
        self.timer    = timer
        self.previous = False
        self.motion   = False
        self.rttp     = RTTP(lamps.local.uuid)

    def handle(self):
        self.motion = pin2.read_analog() > 500       
        if self.previous == self.motion:
            if self.lamps.isActivated:
                self.timer.time = 3000
        else:
            if self.motion:
                self.rttp.setMessage("ACT")
                self.lamps.local.activated = True
            else:
                self.rttp.setMessage("DEACT")
                self.lamps.local.activated = True
            self.rttp.send()
        

class LightHandler:
    def __init__(self, timer:Timer):
        self.timer   = timer
        self.lightOn = False

    def handle(self):
        if self.timer.time < 0:
            self.lightOn = False
            pin0.write_digital(1)
        else:
            self.lightOn = True
            pin0.write_digital(0)
        

class MessageHandler:
    def __init__(self, lamps: LampCollection, logger: Logger):
        self.logger = logger
        self.lamps  = lamps
        self.rttp   = RTTP(lamps.local.uuid)

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
            self.handleUnknownMethod(message)


    def handleACT(self, message: Message):
        sourceLamp = self.lamps.getById(message.source)
        sourceLamp.activated = True
        if sourceLamp.activator:
            self.lamps.local.iactivated = True
        self.rttp.setMessage("IACT")
        self.rttp.send()

    def handleIACT(self, message: Message):
        sourceLamp = self.lamps.getById(message.source)
        sourceLamp.iactivated = True

    def handleDEACT(self, message: Message):
        sourceLamp = self.lamps.getById(message.source)
        if sourceLamp.activated:
            sourceLamp.activated = False
            sourceLamp.direct += 1
            self.lamps.local.indirect += 1
        if sourceLamp.iactivated:
            sourceLamp.iactivated = False
            sourceLamp.activations.indirect += 1

    def handleGET(self, message):
        pass

    def handlePOST(self, message):
        pass

    def handleUnknownMethod(self, message: Message):
        msg = "{" + message.encode() + "}"
        self.logger.error("Unkown method: " + msg, "fatal")