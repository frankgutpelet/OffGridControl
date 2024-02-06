from OffGridControlRunner import OffGridControlRunner
from InverterAdapter import InverterAdapter
from mylogging import Logging
from VictronReader import VictronReader
from EASun import EASun
from Settings import Settings
from Com import TTYWrapper

def main():
    comports = list()
    settings = Settings('Settings.xml')
    logger = Logging()
    victronCharger1 = TTYWrapper('ttyUSB0', 19200)
    victronCharger2 = TTYWrapper('ttyUSB0', 19200)
    comports.append(victronCharger1)
    comports.append(victronCharger2)
    easun = EASun(logger)

    victron = VictronReader(logger, comports)
    inverter = InverterAdapter(victron, easun)
    runner = OffGridControlRunner('Settings.xml', logger, inverter)



if __name__ == '__main__':
    main()
