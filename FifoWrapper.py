import os
from IFifo import IFifo
from mylogging import Logging
import socket

class FifoWrapper(IFifo):

    def __init__(self, filepath : str, logger : Logging):
        self.filepath = filepath
        self.handle = None
        self.logger = logger
        try:
            os.mkfifo(self.filepath )
        except FileExistsError:
            self.logger.Debug(filepath + " still exists")
        pass

    def open(self):
        pass

    def close(self):
        pass

    def write(self, message: str):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 23456))
                s.sendall(message.encode())
                self.logger.Debug("Send to Frontend: " + message)
        except ConnectionRefusedError:
            s.close()
            self.logger.Debug("Connection to Frontend refused, reconnecting ...")