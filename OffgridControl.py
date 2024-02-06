from OffGridControlRunner import OffGridControlRunner
from InverterAdapter import InverterAdapter
from mylogging import Logging
from VictronReader import VictronReader
from EASun import EASun
from Settings import Settings
from Com import TTYWrapper
from Frontend import Frontend
from FifoWrapper import FifoWrapper

def main():
    comports = list()
    settings = Settings('Settings.xml')
    logger = Logging()
    logger.setLogLevel(settings.logging.loglevel, False)
    victronCharger1 = TTYWrapper('/dev/ttyUSB0', 19200, logger)
    victronCharger2 = TTYWrapper('/dev/ttyUSB1', 19200, logger)
    fifo = FifoWrapper('tmp/solarWatcher.fifo')
    frontend = Frontend(fifo, logger)
    comports.append(victronCharger1)
    comports.append(victronCharger2)
    easun = EASun(logger)

    victron = VictronReader(logger, comports)
    inverter = InverterAdapter(victron, easun)
    runner = OffGridControlRunner('Settings.xml', logger, inverter, frontend)
    runner.run()



if __name__ == '__main__':
    main()
