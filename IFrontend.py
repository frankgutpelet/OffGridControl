from abc import ABC, abstractmethod
from mylogging import Logging
from IFifo import IFifo


class IFrontend (ABC):
    transferDataGlobal : list
    transferDataDevice : list

    @abstractmethod
    def __init__(self, fifo : IFifo, logger : Logging):
        raise NotImplementedError()

    @abstractmethod
    def updateDevice(self, transferData : list):
        raise NotImplementedError()

    @abstractmethod
    def updateGlobalData(self, transferData : list):
        raise NotImplementedError()

    @abstractmethod
    def sendData(self):
        raise NotImplementedError()

    @abstractmethod
    def clearDeviceList(self):
        raise  NotImplementedError
