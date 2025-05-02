from IInverter import IInverter
from IVictronReader import IVictronReader
from Daly import Daly

class InverterAdapter(IInverter):
    __victron : IVictronReader
    __victronData : list
    #__easun : IEASun
    __daly : Daly
    __easunStanbyCurrentAmpere = 1

    def __init__(self, victron : IVictronReader, daly : Daly ):
        self.__victron = victron
        self.__victronData = self._chargerData.remove('supply')
        #self.__easun = easun
        self.__daly = daly

    def getChargerData(self):
        data = self.__victron.getValues()
        while not data:
            data = self.__victron.getValues()
        data['supply'] = self.getSupply(data['batI'])
        return data

    def getSupply(self, solarCurrent):
        batteryCurrent = float(self.__daly.getCurrent())
        inverterCurrent = solarCurrent - batteryCurrent
        if (inverterCurrent > self.__easunStanbyCurrentAmpere):
            return "Solar"
        return "Utility"

