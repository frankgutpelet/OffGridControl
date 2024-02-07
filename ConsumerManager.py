from IConsumerManager import IConsumerManager
from IConsumer import IConsumer
from IInverter import IInverter
from mylogging import Logging
from Settings import Settings
from datetime import datetime

class ConsumerManager(IConsumerManager):
    logger : Logging
    inverter : IInverter
    consumers : list
    settings : Settings
    lastSwitchOn : int
    simMode : bool
    inverterData : dict

    def __init__(self, inverter : IInverter, logging : Logging, settings : Settings, simMode = False):
        self.inverter = inverter
        self.logger = logging
        self.consumers = list()
        self.settings = settings
        self.lastSwitchOn = 0
        self.simMode = simMode

    def updateConsumerList(self, consumerList : list):                                                                  #update list of consumers (after configuration change)
        self.consumers.clear()
        for prio in range(10):
            for consumer in consumerList:
                consumer: IConsumer
                if prio == consumer.prio:
                    if self.simMode:
                        consumer.requests = False
                    self.consumers.append(consumer)



    def stayAlive(self):
        self.inverterData = self.inverter.getChargerData()
        self.__MinimumVoltageReached(self.inverterData)

    def manageApprovals(self):                                                                                          #switch all devices depending on mode and inverter state
        inverterData = self.inverter.getChargerData()
        inverterState = self.__getInverterState(inverterData)
        for consumer in self.consumers:
            if self.__MinimumVoltageReached(inverterData):
                return

            if "On" == consumer.mode:
                self.__switchOn(consumer)
                continue
            if "Off" == consumer.mode:
                self.__switchOff(consumer)
                continue

            if Settings.E_SUPPLY.UTILITY == consumer.supply:
                self.__switchOn(consumer)
                continue
            if Settings.E_SUPPLY.BATTERY == consumer.supply and inverterState in [Settings.E_SUPPLY.SURPLUS,
                                                                                  Settings.E_SUPPLY.SOLAR,
                                                                                  Settings.E_SUPPLY.BATTERY]:
                self.__switchOn(consumer)
                continue
            if Settings.E_SUPPLY.SOLAR == consumer.supply and inverterState in [Settings.E_SUPPLY.SURPLUS,
                                                                                Settings.E_SUPPLY.SOLAR]:
                self.__switchOn(consumer)
                continue
            if Settings.E_SUPPLY.SURPLUS == consumer.supply and inverterState == Settings.E_SUPPLY.SURPLUS:
                self.__switchOn(consumer)
                continue
            self.__switchOff(consumer)

    def push(self):                                                                                                     #function to update devices independend from status change
        for consumer in self.consumers:
            consumer.push()


    def __getInverterState(self, inverterData : list()):
        if Settings.E_SUPPLY.UTILITY == inverterData['supply']:
            return Settings.E_SUPPLY.UTILITY
        if Settings.E_SUPPLY.SOLAR == inverterData['supply'] and 2 > inverterData['batI'] and inverterData['chargingstate'] not in ['Abs', 'Float']:
            return Settings.E_SUPPLY.BATTERY
        if Settings.E_SUPPLY.SOLAR == inverterData['supply'] and self.settings.floatVoltage > inverterData['batV']:
            return Settings.E_SUPPLY.SOLAR
        if Settings.E_SUPPLY.SOLAR == inverterData['supply'] and self.settings.floatVoltage <= inverterData['batV']:
            return Settings.E_SUPPLY.SURPLUS

        raise Exception("unknown Inverter State: " + str(inverterData))


    def __MinimumVoltageReached(self, inverterData):
        if inverterData['batV'] < self.settings.inverterMinimumVoltage or Settings.E_SUPPLY.UTILITY == inverterData['supply']:
            for consumer in self.consumers:
                if consumer.prohibit(True):
                    self.logger.Debug("Minimum Voltage reached: switch off " + consumer.name)
                consumer.push()
            return True

    def __switchOn(self, consumer : IConsumer):
        now = datetime.now().timestamp()

        if (0 != self.lastSwitchOn) and (self.settings.switchDelaySeconds > (now - self.lastSwitchOn)):                 # do not switch if the last switch was not long enough ago
            return

        if consumer.isOn:
            return

        if consumer.approve():
            self.logger.Debug("Approve consumer: " + consumer.name)
            consumer.push()                                                                                             #do only a push if a switch happend
            self.lastSwitchOn = datetime.now().timestamp()


    def __switchOff(self, consumer : IConsumer):
        if (consumer.minTime * 60)  > consumer.onTime():                                                                #switch off after minimal runtime
            return
        if not consumer.isOn:
            return
        if consumer.prohibit(False):
            self.logger.Debug("Prohibit consumer: " + consumer.name)
        consumer.push()



