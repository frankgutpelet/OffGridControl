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
import gc

def main():
    comports = list()
    settings = Settings('Settings.xml')
    logger = Logging()
    logger.setLogLevel(settings.logging.loglevel, False)
    ports = glob.glob('/dev/ttyUSB*')
    dalyPort = 2
    dalyBms = None
    for i in reversed(ports):
        tty = i
        if not os.path.exists(tty):
            logger.Error(tty + " not available")
            continue
        victronCharger = TTYWrapper(tty, 19200, logger)
        try:
            victronCharger.connect()
        except:
            logger.Error("Could not open " + i)
            continue
        line = str(victronCharger.readline())
        if "b\'\'" != line:
            logger.Debug("Found victron on Port ttyUSB" + str(i) + ": " + line)
            comports.append(victronCharger)
        elif not dalyBms:

            dalyBms = Daly(TTYWrapper(tty, 9600,logger), logger)
            dalyBms.read()
            if 0 == dalyBms.getVoltage():
                dalyBms = None
                gc.collect()
            else:
                logger.Debug("Found Daly BMS on port " + tty + " Voltage: " + str(dalyBms.getVoltage()) + "V")
        victronCharger.disconnect()

    fifo = FifoWrapper('/tmp/solarWatcher.fifo', logger)
    frontend = Frontend(fifo, logger, dalyBms)
    supplySwitch = SupplySwitch(dalyBms, logger, settings)
    victron = VictronReader(logger, comports)
    inverter = InverterAdapter(victron, dalyBms, supplySwitch)
    runner = OffGridControlRunner('Settings.xml', logger, inverter, frontend, dalyBms)
    runner.run()



if __name__ == '__main__':
    main()
