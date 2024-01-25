from abc import ABC, abstractmethod
from mylogging import Logging

class IVictronReader():

    @abstractmethod
    def __init__(self, logger : Logging, comports: list):
        raise NotImplementedError()

    def getValues(self):
        raise NotImplementedError()