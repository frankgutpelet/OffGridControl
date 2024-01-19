import xml.etree.ElementTree as ET
from datetime import time
from enum import Enum

class Settings:
    class Approval:
        class Supply(Enum):
            SURPLUS = 1
            SOLAR = 2
            BATTERY = 3
            UTILITY = 4

        class status(Enum):
            OFF = 1
            AUTO = 2
            ON = 3

        class timer:
            on : time
            off : time
            isOn : bool

        name : str
        dns : str
        prio : int
        supply = Enum("supply", ["SURPLUS", "SOLAR", "BATTERY", "UTILITY"])
        status = Enum("status", ["OFF", "AUTO", "ON"])
        timers : list()

    class Logging:

        validLoglevels = ["DEBUG", "ERROR", "INFO"]
        loglevel : str
        logFile : str

        def __init__(self, loglevel : str, logfile : str):

            self.loglevel = ""
            for validLoglevel in self.validLoglevels:
                if validLoglevel == loglevel:
                    self.loglevel = loglevel

            if "" == self.loglevel:
                raise Exception(loglevel + " is no valid loglevel")

            self.loglevel = loglevel
            self.logFile = logfile




            self.logFile = logfile = logfile

        def getLoglevel(self):
            return self.__logLevelText[self.__loglevel]

    logging : Logging


    def __init__(self, logfile : str):
        tree = ET.parse(logfile)
        root = tree.getroot()

        tagLogging = root.find("Logging")
        self.logging = self.Logging(tagLogging.attrib['loglevel'], tagLogging.attrib['file'])

        self.logging = self.logging






    approvals : list()

