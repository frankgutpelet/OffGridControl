from abc import ABC, abstractmethod
from mylogging import Logging

class IEASun():

    @abstractmethod
    def __init__(self, logger : Logging):
        raise NotImplementedError()

    def getMode(self):
        raise NotImplementedError()