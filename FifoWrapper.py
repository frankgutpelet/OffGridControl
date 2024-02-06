import os
from IFifo import IFifo
from mylogging import Logging

class FifoWrapper(IFifo):

    def __init__(self, filepath : str, logger : Logging):
        self.filepath = filepath
        self.handle = None
        self.logger = logger
        try:
            os.mkfifo(self.filepath)
        except FileExistsError:
            self.logger.Debug(filepath + " still exists")
        pass

    def open(self):
        self.handle =  open(self.filepath, "w")

    def close(self):
        if self.handle:
            return self.handle.close()
        return None

    def write(self, message: str):
        if self.handle:
            return self.handle.write(message)
        raise Exception("invalid filehandle for Fifo")