from abc import ABC, abstractmethod
from IInverter import IInverter
from IConsumer import IConsumer
from mylogging import Logging
from Settings import Settings

class IConsumerManager(ABC):
    @abstractmethod
    def __init__(self, inverter : IInverter, logging : Logging, settings : Settings):
        raise NotImplementedError()

    @abstractmethod
    def updateConsumerList(self, consumerList : list):
        raise NotImplementedError()

    @abstractmethod
    def manageApprovals(self):
        raise NotImplementedError()