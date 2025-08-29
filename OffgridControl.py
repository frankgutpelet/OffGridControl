from OffGridControlRunner import OffGridControlRunner
from InverterAdapter import InverterAdapter
from mylogging import Logging
from VictronReader import VictronReader
from Settings import Settings
from Frontend import Frontend
from FifoWrapper import FifoWrapper
from SupplySwitch import SupplySwitch
from SerialFactory import SerialFactory

def main():
    numberOfVictrons = 2

    settings = Settings('Settings.xml')
    logger = Logging()
    logger.setLogLevel(settings.logging.loglevel, False)
    serialFactory = SerialFactory(numberOfVictrons, logger)
    dalyBms = serialFactory.getDalyBms()

    fifo = FifoWrapper('/tmp/solarWatcher.fifo', logger)
    frontend = Frontend(fifo, logger, dalyBms)
    supplySwitch = SupplySwitch(dalyBms, logger, settings)
    victron = VictronReader(logger, serialFactory.getVictrons())
    inverter = InverterAdapter(victron, dalyBms, supplySwitch)
    runner = OffGridControlRunner('Settings.xml', logger, inverter, frontend, dalyBms)
    runner.run()



if __name__ == '__main__':
    main()
