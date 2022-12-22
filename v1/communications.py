import radio
import machine
from models import Message

radio.config(
    length=251,
    queue=20,
    channel=69,
    power=7,
    address=0x69420666,
    group=69
)
radio.on

class RTTP:
    def __init__(self, uuid):
        self.uuid = uuid
        self.message = Message()
        self.last_request  = ""
        self.last_response = ""

    def send(self):
        self.last_request = self.message.encode()
        radio.send(self.last_request)

    def nextMessage(self):
        response = radio.receive()
        if response:
            self.last_response = response
            self.message.parse(self.last_response)
            return True
        return False

    def setMessage(self, method, data = "", recipient = "ALL"):
        self.message.method    = method
        self.message.source    = self.uuid
        self.message.recipient = recipient
        self.message.data      = data
