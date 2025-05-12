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
        self.handle = None

    def flush(self):
        if not self.handle:
            return b''
        return self.handle.flush()

    def readline(self):
        if not self.handle:
            return b''
        return self.handle.readline()

    def write(self, bytes):
        if not self.handle:
            return b''
        self.handle.write(bytes)

    def read(self, noBytes):
        if not self.handle:
            return b''
        return self.handle.read(noBytes)

    def connect(self):
        try:
            self.handle = Serial(self.com, self.baud, timeout=5)
            if not self.handle:
                raise Exception("connection to serial Port failed - no handle")
        except Exception as e:
            self.logger.Error(f"No connection to serial port {self.com}: {e}")
            return None
        self.logger.Debug(f"Connected to {self.com} with {self.baud}")
        return self.handle

    def disconnect(self):
        if not self.handle:
            return
        return self.handle.close()

    def isOpen(self):
        return self.handle.isOpen()