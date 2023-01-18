import radio
from models import Message
from logger import Logger
from app import *

radio.config(
    length=251,
    queue=20,
    channel=69,
    power=7,
    address=0x69420666,
    group=69
)
radio.on

class MessageHandler():
    def __init__(self, app):
        self.app = app

    def handle(self):
        while (True):
            message = self.app.rttp.nextMessage()
            if not message:
                break
            
            if message.recipient != "ALL" and message.recipient != self.app.lamps.local.uuid:
                continue
                   
            if message.method == "ACT":
                self.handleACT(message)
            elif message.method == "IACT":
                self.handleIACT(message)
            elif message.method == "DEACT":
                self.handleDEACT(message)
            else:
                self.handleUnknownMethod(message)


    def handleACT(self, message: Message):
        self.app.logger.general("MessageHandler - handleACT()")
        sourceLamp = self.app.lamps.getById(message.source)
        sourceLamp.activated    = True
        sourceLamp.activations += 1
        self.app.lamps.set(sourceLamp)
        if sourceLamp.activator:
            self.app.lamps.local.iactivated = True
        self.app.rttp.setMessage("IACT")
        self.app.rttp.send()

    def handleIACT(self, message: Message):
        self.app.logger.general("MessageHandler - handleIACT()")
        sourceLamp = self.app.lamps.getById(message.source)
        sourceLamp.iactivated = True

    def handleDEACT(self, message: Message):
        self.app.logger.general("MessageHandler - handleDEACT()")
        sourceLamp = self.app.lamps.getById(message.source)
        if sourceLamp.activated:
            sourceLamp.activated = False
            sourceLamp.iactivated = False
        self.app.lamps.set(sourceLamp)

    def handleUnknownMethod(self, message: Message):
        self.app.logger.general("MessageHandler - handleUnknownMethod()")
        msg = "'" + message.encode() + "'"
        self.app.logger.error("Unkown method: " + msg, "fatal")                
                

class RTTP:
    def __init__(self, uuid, logger: Logger):
        self.uuid          = uuid
        self.message       = Message()
        self.last_request  = ""
        self.last_response = ""
        self.logger        = logger

    def send(self):
        self.last_request = self.message.encode()
        radio.send(self.last_request)
        self.logger.network("RTTP - Message sent", self.last_request)

    def nextMessage(self):
        response = radio.receive()
        if response:
            self.last_response = response
            self.logger.network("RTTP - Message received", response)
            return self.message.parse(self.last_response)
        return False

    def setMessage(self, method, data = "", recipient = "ALL"):
        self.message.method    = method
        self.message.source    = self.uuid
        self.message.recipient = recipient
        self.message.data      = data
