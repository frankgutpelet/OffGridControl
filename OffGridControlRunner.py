from Settings import Settings
from mylogging import Logging
import traceback, time, os
from ConsumerManager import ConsumerManager
from IInverter import IInverter
from Consumer import Consumer

class OffGridControlRunner:
    settingsFile : str
    logger : Logging
    settings : Settings
    manager : ConsumerManager
    settingsTimestamp : int
    inverter: IInverter

    def __init__(self, settings : str, logger : Logging, inverter : IInverter, simMode = False):
        self.settingsFile =settings
        self.logger = logger
        self.settingsTimestamp = 0

        self.inverter = inverter
        self.manager = ConsumerManager(inverter, logger, Settings(self.settingsFile), simMode)
        self._checkSettings()

    def run(self):
        while(True):
            try:
                self.__thread()
            except:
                self.logger.Error("Exception occured, restart thread:\n" + traceback.format_exc())
                time.sleep(30)


    def __thread(self):
        self._checkSettings()
        for run in range(100):
            self.manager.stayAlive()
        self.manager.manageApprovals()

    def _checkSettings(self):
        if self.settingsTimestamp != os.path.getmtime(self.settingsFile):
            self.settingsTimestamp = os.path.getmtime(self.settingsFile)
            self.settings = Settings(self.settingsFile)
            consumers = list()
            for approval in self.settings.approvals:
                consumers.append(Consumer(approval, self.logger))
            self.manager.updateConsumerList(consumers)

