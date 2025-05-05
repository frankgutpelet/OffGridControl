from IInverter import IInverter
from IVictronReader import IVictronReader
from Daly import Daly
from SupplySwitch import SupplySwitch

class InverterAdapter(IInverter):
    __victron : IVictronReader
    __victronData : list
    #__easun : IEASun
    __daly : Daly
    __easunStanbyCurrentAmpere = 1
    __suplySwitch : SupplySwitch

    def __init__(self, victron : IVictronReader, daly : Daly, switch : SupplySwitch ):
        self.__victron = victron
        self.__victronData = self._chargerData.remove('supply')
        #self.__easun = easun
        self.__daly = daly
        self.__suplySwitch = switch

    def getChargerData(self):
        data = self.__victron.getValues()
        while not data:
            data = self.__victron.getValues()
        data['supply'] = self.getSupply(data['batI'])
        return data

    def getSupply(self, solarCurrent):
        if "ON" == self.__suplySwitch.switchState:
            return "Solar"
        else:
            return "Utility"

