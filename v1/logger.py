import log

class Logger:
    def __init__(self, clock):
        self.clock = clock
        log.set_mirroring(False)
        log.set_labels(
            'log',
            'timestamp',
            'type',
            'message',
            'data',
            timestamp=None
        )

    def error(self, message, data = "", type = "warning"):
        self.add('error', type, message, data)
        
    def general(self, message, data = "", type = "info"):
        self.add('general', type, message, data)

    def network(self, message, data = "", type = "info"):
        self.add('network', type, message, data)
        
    def add(self, logname, type, message, data):
        log.add({
            'log': logname,
            'timestamp': self.clock.datetime.__repr__(),
            'type': type,
            'message': message,
            'data': data
        })