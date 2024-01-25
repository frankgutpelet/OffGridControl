from IInverter import IInverter
from IVictronReader import IVictronReader
from IEASun import IEASun

class InverterAdapter(IInverter):
    __victron : IVictronReader
    __victronData : list
    __easun : IEASun

    def __init__(self, victron : IVictronReader, easun : IEASun ):
        self.__victron = IVictronReader
        self.__victronData = self._chargerData.remove('supply')
        self.__easun = easun

    def getChargerData(self):
        data = self.__victron.getValues()
        data['supply'] = self.__easun.getMode()