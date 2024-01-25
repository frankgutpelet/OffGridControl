from abc import ABC, abstractmethod

class ICom(ABC):
    @abstractmethod
    def __init__(self, com : str, baud : int):
        raise NotImplementedError()

    @abstractmethod
    def flush(self):
        raise NotImplementedError()

    @abstractmethod
    def readline(self):
        raise NotImplementedError()

    @abstractmethod
    def connect(self):
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError

    @abstractmethod
    def isOpen(self):
        raise NotImplementedError