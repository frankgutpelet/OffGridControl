from abc import ABC, abstractmethod
from IInverter import IInverter
from IConsumer import IConsumer
from mylogging import Logging

class IConsumerManager(ABC):
    @abstractmethod
    def __init__(self, inverter : IInverter, logging : Logging):
        raise NotImplementedError()

    @abstractmethod
    def updateConsumers(self, consumerList : list(IConsumer)):
        raise NotImplementedError()