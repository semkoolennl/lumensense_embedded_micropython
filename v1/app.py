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

        self.motionHandler  = MotionHandler(self.lamps, self.logger)
        self.lightHandler   = LightHandler(self.lamps, self.logger)
    
    def run(self):
        self.clock.tick()
        self.timer.update(self.clock.lastTick)    
    
        self.motionHandler.handle()
    
        if self.motionHandler.resetTimer:
            self.timer.time = 3000
    
        self.lightHandler.handle(self.timer)

    def getTime(self):
        return str(self.clock.datetime)

    def setTime(self, timeString):
        try:  
            self.clock.datetime.fromString(timeString)
            return "success"
        except:
            return "error: incorrect format"
        

    def getUUID(self):
        return self.uuid

    def setUUID(self, uuid):
        self.uuid = uuid
        self.rttp.uuid = uuid
        self.lamps.local.uuid = uuid
        return "success"

    def getActivators(self):
        return ",".join([uuid for uuid in self.lamps.getAll()])

    def setActivators(self, activators):
        for uuid in self.lamps.lamps:
            self.lamps.getById(uuid).activator = False
        for uuid in activators.split(",")[:-1]:
            self.lamps.getById(uuid).activator = True
        return "success"

    def getActivations(self):
        activators = []
        for uuid in self.lamps.getAll():
            lamp = self.lamps.getById(uuid)
            activators.append(uuid + "=" + str(lamp.activations.direct) + "|" + str(lamp.activations.indirect))
        return ",".join(activators)

    def getStatus(self):
        status = []
        for uuid in self.lamps.getAll():
            lamp = self.lamps.getById(uuid)
            status.append(uuid + "=" + str(lamp.activated | lamp.iactivated))
        return ",".join(status)
        
            
            