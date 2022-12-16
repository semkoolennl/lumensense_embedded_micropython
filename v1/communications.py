import radio
import machine

radio.config(
    length=251,
    queue=20,
    channel=69,
    power=7,
    address=0x69420666,
    group=69
)
radio.on


class rttp:
    def __init__(self, uuid):
        self.uuid = uuid
        self.last_request = ""
        self.last_response = ""

    def send(self, method, recipient="ALL", data=""):
        self.last_request = recipient + ";" + method + ";" + data
        radio.send(self.last_request)

    def nextMessage(self):
        response = radio.receive()
        if response:
            self.last_response = response
            return True
        return False

    def sendACT(self, recipient="ALL"):
        self.send("ACT", recipient)

    def sendDEACT(self, recipient="ALL"):
        self.send("DEACT", recipient)

    def sendIACT(self, recipient="ALL"):
        self.send("IACT", recipient)
