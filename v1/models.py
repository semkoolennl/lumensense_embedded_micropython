class Lamp:
    def __init__(self, uuid: str, activator: bool = False):
        self.uuid        = uuid
        self.activated   = False
        self.iactivated  = False
        self.activator   = activator
        self.activations = Activations()
        

class LampCollection:
    def __init__(self, localLamp):
        self.local = localLamp
        self.lamps = {}

    def add(self, lamp: Lamp):
        self.lamps[lamp.uuid] = lamp

    def getById(self, uuid: str):
        return self.lamps[uuid]

    def set(self, lamp):
        self.lamps[lamp.uuid] = lamp

    def setActivated(self, bool, uuid):
        self.lamps[uuid] = bool

    def isActivated(self):
        for name in self.lamps:
            lamp = self.lamps[name]
            if lamp.activated and lamp.activator:
                return True
        return self.local.activated
        
        
class Activations:
    def __init__(self, direct = 0, indirect = 0):
        self.direct   = direct
        self.indirect = indirect

    def reset(self):
        self.direct   = 0
        self.indirect = 0

        
class Message:
    def __init__(self):
        self.method    = ""
        self.source    = ""
        self.recipient = ""
        self.data      = ""

    def set(self, method, source, recipient, data):
        self.method    = method
        self.source    = source
        self.recipient = recipient
        self.data      = data

    def encode(self):
        return self.__repr__()

    def parse(self, string):
        arr = string.split(";")
        self.method    = arr[0]
        self.source    = arr[1]
        self.recipient = arr[2]
        self.data      = arr[3]

        return self

    def __repr__(self):
        return ';'.join([
            self.method,
            self.source,
            self.recipient,
            self.data
        ])