import uarray
from microbit import *

uart.init(115200, 8)
uart.ODD

class SerialHandler:
    def __init__(self, app):
        self.app    = app
        self.reader = MessageReader(uart)

    def handle(self):
        if (uart.any()):
            raw = self.reader.read_message()
            uart.write("ACK;"+raw+"\n")
            request = Request()
            request.parse(raw)
            response = False
            try:
                if (request.method == "GET"):
                    response = self.handleGET(request)
                elif (request.method == "POST"):
                    response = self.handlePOST(request)
                    
                if not response:
                    response = "Error: Unknown method"
            except:
                response = "Error: Unknown error serial handle"
            request.payload = response
            uart.write(request.encode() + "\n")
                    
    def handleGET(self, request):
        response = False;
        if request.action == "LOG":
            response = self.app.getLog()
        if request.action == "ACTIVATIONS":
            response = self.app.getActivations()
        if request.action == "STATUSSES":
            response = self.app.getStatus()
        if request.action == "TestConnection":
            return "success"
        if not response:
            response = "Error: Unknown action"
        return response

    def handlePOST(self, request):
        response = False
        if request.action == "TIME":
            response = self.app.setTime(request.payload)
        if not response:
            response = "Error: Unknown action"
        return response

            
            

class MessageReader:
    def __init__(self, uart):
        self.uart = uart
        self.buf = bytearray(1)
        self.message = bytearray()

    def read_message(self):
        while True:
            nbytes = self.uart.readinto(self.buf)
            if nbytes == 0:
                continue
            if self.buf[0] == ord('\n'):
                message = uarray.array('B', self.message).decode()
                self.message = bytearray()
                return message
            else:
                self.message.append(self.buf[0])

class Request:
    def __init__(self):
        self.method  = ""
        self.action  = ""
        self.payload = ""

    def encode(self):
        return ";".join([
            str(self.method),
            str(self.action),
            str(self.payload)
        ])

    def parse(self, string):
        arr = string.split(";")
        self.method  = arr[0]
        self.action  = arr[1]
        if (len(arr) > 2):
            self.payload = arr[2]

        return self

    
        
            