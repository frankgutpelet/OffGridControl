from Settings import Settings
from mylogging import Logging
import traceback, time, os
from ConsumerManager import ConsumerManager
from IInverter import IInverter
from Consumer import Consumer
from IFrontend import IFrontend

class OffGridControlRunner:
    settingsFile : str
    logger : Logging
    settings : Settings
    manager : ConsumerManager
    settingsTimestamp : int
    inverter: IInverter
    frontend : IFrontend

    def __init__(self, settings : str, logger : Logging, inverter : IInverter, frontend : IFrontend, simMode = False):
        self.settingsFile =settings
        self.logger = logger
        self.settingsTimestamp = 0
        self.frontend = frontend
        self.inverter = inverter
        self.manager = ConsumerManager(inverter, logger, Settings(self.settingsFile), simMode)
        self._checkSettings()

    def run(self):
        while(True):
            try:
                self.__thread()
            except:
                self.logger.Error("Exception occured, restart thread:\n" + traceback.format_exc())
                time.sleep(10)


    def __thread(self):
        for run in range(10):
            self.manager.stayAlive()
            time.sleep(1)
            if self._checkSettings():
                self.logger.Debug("reload Settings - File Changed")
                self.manager.settings = self.settings
                break
        self.manager.manageApprovals()
        self.manager.push()
        self.__updateFrontend()





    def __updateFrontend(self):
        globalData = dict()
        for key in self.frontend.transferDataGlobal:
            globalData[key] = self.manager.inverterData[key]
        self.frontend.updateGlobalData(globalData)
        for consumer in self.manager.consumers:
            state = 'Off'
            if consumer.isOn:
                state = 'On'
            self.frontend.updateDevice(
                {'name': consumer.name, 'state': state, 'mode': consumer.mode, 'ontime': str(consumer.onTime())})
        self.frontend.sendData()

    def _checkSettings(self):
        if self.settingsTimestamp != os.path.getmtime(self.settingsFile):
            self.settingsTimestamp = os.path.getmtime(self.settingsFile)
            self.settings = Settings(self.settingsFile)
            consumers = list()
            for approval in self.settings.approvals:
                consumers.append(Consumer(approval, self.logger))
            self.manager.updateConsumerList(consumers)
            self.frontend.clearDeviceList()
            return True

        return False

