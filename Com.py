from ICom import ICom
from serial import Serial

class TTYWrapper(ICom):
    com : str
    baud : int
    handle : object

    def __init__(self, com : str, baud : int):
        self.com = com
        self.baud = baud

    def flush(self):
        return self.handle.flush()

    def readline(self):
        return self.handle.readline()

    def connect(self):
        self.handle = Serial(self.com, self.baud)
        return self.handle

    def disconnect(self):
        return self.handle.close()

    def isOpen(self):
        return self.handle.isOpen()