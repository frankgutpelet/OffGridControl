from OffGridControlRunner import OffGridControlRunner
from InverterAdapter import InverterAdapter
from mylogging import Logging
from VictronReader import VictronReader
from EASun import EASun
from Settings import Settings
from Com import TTYWrapper
from Frontend import Frontend
from FifoWrapper import FifoWrapper
from SupplySwitch import SupplySwitch
from Daly import Daly
import glob
import os

def main():
    comports = list()
    settings = Settings('Settings.xml')
    logger = Logging()
    logger.setLogLevel(settings.logging.loglevel, False)
    ports = glob.glob('/dev/ttyUSB*')
    dalyPort = 2
    for i in ports:
        tty = i
        if not os.path.exists(tty):
            logger.Error(tty + " not available")
            continue
        victronCharger = TTYWrapper(tty, 19200, logger)
        victronCharger.connect()
        line = str(victronCharger.readline())
        if "b\'\'" != line:
            logger.Debug("Found victron on Port ttyUSB" + str(i) + ": " + line)
            comports.append(victronCharger)
        else:
            dalyPort = i
        victronCharger.disconnect()

    dalyBms = Daly(TTYWrapper(dalyPort, 9600,logger), logger)
    logger.Debug("Found Daly on port ttyUSB" + str(dalyPort))
    fifo = FifoWrapper('/tmp/solarWatcher.fifo', logger)
    frontend = Frontend(fifo, logger, dalyBms)
    supplySwitch = SupplySwitch(dalyBms, logger, settings)
    victron = VictronReader(logger, comports)
    inverter = InverterAdapter(victron, dalyBms, supplySwitch)
    runner = OffGridControlRunner('Settings.xml', logger, inverter, frontend, dalyBms)
    runner.run()



if __name__ == '__main__':
    main()
