from communications import *
from handlers import *
from logger import *
from models import *
from timeutils import *

class App:
    def __init__(self, uuid, datetime):
        self.uuid   = uuid
        self.clock  = Clock(datetime)
        self.timer  = Timer()
        self.logger = Logger(self.clock)
        self.rttp   = RTTP(self.uuid, self.logger)
        self.setup()

    def setup(self):
        lamp  = Lamp(self.uuid)
        self.lamps = LampCollection(lamp)
    
    def run(self):
        self.clock.tick()
        self.timer.update(self.clock.lastTick)    
    
    def setTime(self, timeString):
        try:  
            self.clock.datetime.fromString(timeString)
            return "success"
        except:
            return "error: incorrect format"

    
    def getActivations(self):
        activations = []
        for uuid in self.lamps.getAll():
            lamp = self.lamps.getById(uuid)
            activations.append(uuid + "=" + str(lamp.activations))
        return ",".join(activations)

    def getStatus(self):
        status = []
        for uuid in self.lamps.getAll():
            lamp = self.lamps.getById(uuid)
            status.append(uuid + "=" + str(lamp.activated | lamp.iactivated))
        return ",".join(status)
        
            
            