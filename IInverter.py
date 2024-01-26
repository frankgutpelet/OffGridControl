from abc import ABC, abstractmethod

class IInverter(ABC):
    _chargerData = {'batV', 'batI', 'solV', 'todayE', 'yesterdayE', 'supply', 'charchingstate'}
    @abstractmethod
    def __init__(self):
        raise NotImplementedError()
    @abstractmethod
    def getChargerData(self):
        raise NotImplementedError()