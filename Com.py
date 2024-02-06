from ICom import ICom
from serial import Serial
from mylogging import Logging

class TTYWrapper(ICom):
    com : str
    baud : int
    handle : object
    logger : Logging

    def __init__(self, com : str, baud : int, logger : Logging):
        self.com = com
        self.baud = baud
        self.logger = logger

    def flush(self):
        return self.handle.flush()

    def readline(self):
        return self.handle.readline()

    def connect(self):
        try:
            self.handle = Serial(self.com, self.baud)
            if not self.handle:
                raise Exception("connection to serial Port failed - no handle")
        except:
            self.logger.Error("No connection to serial port " + self.com)
            return None
        self.logger.Debug("Connected to " + self.com + " with " + str(self.baud))
        return self.handle

    def disconnect(self):
        return self.handle.close()

    def isOpen(self):
        return self.handle.isOpen()