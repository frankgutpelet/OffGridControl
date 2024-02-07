from abc import ABC, abstractmethod
from xml.etree.ElementTree import Element

class IConsumer(ABC):
    prio : int
    supply : str #Settings.E_SUPPLY
    mode : str # Settings.E_MODE
    name : str
    isOn: bool
    minTime : int

    @abstractmethod
    def __init__(self, settings : Element):
        raise NotImplementedError()

    @abstractmethod
    def approve(self):
        raise NotImplementedError()

    @abstractmethod
    def prohibit(self, force : bool):
        raise NotImplementedError()

    @abstractmethod
    def push(self):
        raise NotImplementedError()

    @abstractmethod
    def onTime(self):
        raise NotImplementedError()