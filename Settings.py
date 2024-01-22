import xml.etree.ElementTree as ET
from datetime import time

class Settings:
    class E_SUPPLY:
        SURPLUS = 'Surplus'
        SOLAR = 'Solar'
        BATTERY = 'Battery'
        UTILITY = 'Utility'
        names = [SURPLUS, SOLAR, BATTERY, UTILITY]

    class E_STATE:
        ON = 'On'
        OFF = 'Off'
        AUTO = 'Auto'
        names = [ON, OFF, AUTO]
    class Element:
        def _getByStr(self, name : str, enum : list):
            for value in enum:
                if name.upper() == value.upper():
                    return value

    class Approval(Element):
        class timer:
            on : time
            off : time
            isOn : bool

        name : str
        dns : str
        prio : int
        supply : str
        status : str
        timers : list()

        def __init__(self, config : ET.Element):
            self.name = config.attrib['name']
            self.dns = config.attrib['dns']
            self.prio = int(config.attrib['prio'])
            self.supply = self._getByStr(config.attrib['supply'], Settings.E_SUPPLY.names)
            self.status = self._getByStr(config.attrib['status'], Settings.E_STATE.names)

        def Supply(self):
            return self.ENUM_SUPPLY[self.supply]


    class Logging(Element):

        __validLoglevels = ["DEBUG", "ERROR", "INFO"]
        loglevel : int
        __logFile : str

        def __init__(self, loglevel : str, logfile : str):

            self.loglevel = self._getByStr(loglevel, self.__validLoglevels)
            self.__logFile = logfile
            self.__logFile = logfile = logfile

    logging : Logging
    approvals : list[Approval]


    def __init__(self, logfile : str):
        self.approvals = list()

        tree = ET.parse(logfile)
        root = tree.getroot()

        tagLogging = root.find("Logging")
        self.logging = self.Logging(tagLogging.attrib['loglevel'], tagLogging.attrib['file'])


        for app in root.find('Approvals').findall('App'):
            self.approvals.append(self.Approval(app))

    def getApproval(self, name : str):
        for app in self.approvals:
            if app.name == name:
                return app

        return None





    approvals : list()

