from IInverter import IInverter
from IVictronReader import IVictronReader
from IEASun import IEASun
from Daly import Daly

class InverterAdapter(IInverter):
    __victron : IVictronReader
    __victronData : list
    __easun : IEASun
    __daly : Daly

    def __init__(self, victron : IVictronReader, easun : IEASun, daly : Daly ):
        self.__victron = victron
        self.__victronData = self._chargerData.remove('supply')
        self.__easun = easun
        self.__daly = daly

    def getChargerData(self):
        data = self.__victron.getValues()
        while not data:
            data = self.__victron.getValues()
        data['supply'] = self.__easun.getMode()
        return data