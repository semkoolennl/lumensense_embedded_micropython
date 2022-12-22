import log

class Logger:
    def __init__(self, clock):
        self.clock = clock
        log.set_labels(
            'log',
            'timestamp',
            'type',
            'message',
            timestamp=None
        )

    def error(self, message, type = "warning"):
        self.add('error', type, message)
        
    def general(self, message, type = "info"):
        self.add('general', type, message)

    def network(self, message, type = "info"):
        self.add('network', type, message)
        
    def add(self, log, type, message):
        log.add({
            'log': log,
            'timestamp': self.clock.datetime.__repr__(),
            'type': type,
            'message': message,
        })