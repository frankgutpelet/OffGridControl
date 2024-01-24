from abc import ABC, abstractmethod

class IFifo(ABC):
    @abstractmethod
    def __init__(self, filepath : str):
        raise NotImplementedError()

    @abstractmethod
    def open(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def write(self, message: str):
        raise NotImplementedError()
