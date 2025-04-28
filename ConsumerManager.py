from IConsumerManager import IConsumerManager
from IConsumer import IConsumer
from IInverter import IInverter
from mylogging import Logging
from Settings import Settings
from datetime import datetime
from Daly import Daly

class ConsumerManager(IConsumerManager):
    logger : Logging
    inverter : IInverter
    consumers : list
    settings : Settings
    lastSwitchOn : int
    simMode : bool
    inverterData : dict
    dalyBms : Daly

    def __init__(self, inverter : IInverter, logging : Logging, settings : Settings, daly : Daly, simMode = False):
        self.inverter = inverter
        self.logger = logging
        self.consumers = list()
        self.settings = settings
        self.lastSwitchOn = 0
        self.simMode = simMode
        self.logger.Debug("start Consumer Manager")
        self.dalyBms = daly

    def updateConsumerList(self, consumerList : list):                                                                  #update list of consumers (after configuration change)
        self.consumers.clear()
        self.logger.Debug("Update Consumer list")
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
        self.logger.Debug("Inverterstate: " +  inverterState)
        for consumer in self.consumers:

            if "On" == consumer.mode:
                if self.__switchOn(consumer):
                    return
                continue
            if "Off" == consumer.mode:
                if self.__switchOff(consumer):
                    return
                continue

            if Settings.E_SUPPLY.UTILITY == consumer.supply:
                if self.__switchOn(consumer):
                    return
                continue
            if Settings.E_SUPPLY.BATTERY == consumer.supply and inverterState == Settings.E_SUPPLY.BATTERY \
                and consumer.soc > self.dalyBms.getSOC():
                if self.__switchOff(consumer):
                    return
                continue
            if Settings.E_SUPPLY.BATTERY == consumer.supply and inverterState in [Settings.E_SUPPLY.SURPLUS,
                                                                                  Settings.E_SUPPLY.SOLAR,
                                                                                  Settings.E_SUPPLY.BATTERY]:
                if self.__switchOn(consumer):
                    return
                continue
            if Settings.E_SUPPLY.SOLAR == consumer.supply and inverterState in [Settings.E_SUPPLY.SURPLUS,
                                                                                Settings.E_SUPPLY.SOLAR]:
                if self.__switchOn(consumer):
                    return
                continue
            if Settings.E_SUPPLY.SURPLUS == consumer.supply and inverterState == Settings.E_SUPPLY.SURPLUS:
                if self.__switchOn(consumer):
                    return
                continue

        for consumer in reversed(self.consumers):
            if consumer.isOn and consumer.timeswitch and not consumer.timeswitch.isOn(datetime.now().time()):
                self.__switchOff(consumer)

            if Settings.E_SUPPLY.BATTERY == consumer.supply and inverterState not in [Settings.E_SUPPLY.SURPLUS,
                                                                                  Settings.E_SUPPLY.SOLAR,
                                                                                  Settings.E_SUPPLY.BATTERY]:
                self.logger.Debug("Sitch off " + consumer.name + " SupplyState: " + inverterState)
                if self.__switchOff(consumer):
                    return
                continue
            if Settings.E_SUPPLY.SOLAR == consumer.supply and inverterState not in [Settings.E_SUPPLY.SURPLUS,
                                                                                Settings.E_SUPPLY.SOLAR]:
                self.logger.Debug("Sitch off " + consumer.name + " SupplyState: " + inverterState)
                if self.__switchOff(consumer):
                    return
                continue
            if Settings.E_SUPPLY.SURPLUS == consumer.supply and inverterState != Settings.E_SUPPLY.SURPLUS:
                self.logger.Debug("Sitch off " + consumer.name + " SupplyState: " + inverterState)
                if self.__switchOff(consumer):
                    return
                continue

    def push(self):                                                                                                     #function to update devices independend from status change
        for consumer in self.consumers:
            consumer.push()


    def __getInverterState(self, inverterData : list()):
        self.logger.Debug("Inverter: " + str(inverterData['chargingstate']))
        soc = 0
        if '' == self.dalyBms.getSOC():
            self.dalyBms.read()
        if '' != self.dalyBms.getSOC():
            soc = int(self.dalyBms.getSOC())
        self.logger.Debug("SOC: " + str(soc))
        if Settings.E_SUPPLY.SOLAR == inverterData['supply'] and inverterData['chargingstate']  in ['Absorption', 'Float']:
            return Settings.E_SUPPLY.SURPLUS
        if Settings.E_SUPPLY.UTILITY == inverterData['supply']:
            return Settings.E_SUPPLY.UTILITY
        if Settings.E_SUPPLY.SOLAR == inverterData['supply'] and 20 > int(self.dalyBms.getSOC()):
            return Settings.E_SUPPLY.UTILITY
        if Settings.E_SUPPLY.SOLAR == inverterData['supply'] and 70 > int(self.dalyBms.getSOC()):
            return Settings.E_SUPPLY.BATTERY
        if Settings.E_SUPPLY.SOLAR == inverterData['supply'] and 90 > int(self.dalyBms.getSOC()):
            return Settings.E_SUPPLY.SOLAR
        if Settings.E_SUPPLY.SOLAR == inverterData['supply'] and 90 <= int(self.dalyBms.getSOC()):
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
            return False

        if consumer.isOn:
            return False

        if consumer.approve():
            self.logger.Debug("Approve consumer: " + consumer.name)
            consumer.push()                                                                                             #do only a push if a switch happend
            self.lastSwitchOn = datetime.now().timestamp()
            return True
        return False



    def __switchOff(self, consumer : IConsumer):
        if (consumer.minTime * 60)  > consumer.onTime():                                                                #switch off after minimal runtime
            return False
        if not consumer.isOn:
            return False
        if consumer.prohibit(False):
            self.logger.Debug("Prohibit consumer: " + consumer.name)
            consumer.push()
            return True




