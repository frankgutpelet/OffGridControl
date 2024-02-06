import xml.etree.ElementTree as ET
from datetime import time

class Settings:
    class E_SUPPLY:
        SURPLUS = 'Surplus'
        SOLAR = 'Solar'
        BATTERY = 'Battery'
        UTILITY = 'Utility'
        names = [SURPLUS, SOLAR, BATTERY, UTILITY]

    class E_MODE:
        ON = 'On'
        OFF = 'Off'
        AUTO = 'Auto'
        names = [ON, OFF, AUTO]
    class Element:
        def _getByStr(self, name : str, enum : list):
            for value in enum:
                if name.upper() == value.upper():
                    return value

    class Timer:
        onTime : time
        offTime : time
        def __init__(self, onTime : str, offTime : str):
            self.onTime = time(int(onTime.split(':')[0]), int(onTime.split(':')[1]))
            self.offTime = time(int(offTime.split(':')[0]), int(offTime.split(':')[1]))

    class Approval(Element):

        name : str
        dns : str
        prio : int
        supply : str
        mode : str
        timers : list
        minTimeRunningMinutes : int

        def __init__(self, config : ET.Element):
            self.name = config.attrib['name']
            self.dns = config.attrib['dns']
            self.prio = int(config.attrib['prio'])
            self.supply = self._getByStr(config.attrib['supply'], Settings.E_SUPPLY.names)
            self.mode = self._getByStr(config.attrib['mode'], Settings.E_MODE.names)
            if ('minTimeRunningMinutes' in config.attrib):
                self.minTimeRunningMinutes = config.attrib['minTimeRunningMinutes']
            else:
                self.minTimeRunningMinutes = 0
            self.timers = list()
            for timerConfig in config.findall('Timer'):
                self.timers.append(Settings.Timer(timerConfig.attrib['on'], timerConfig.attrib['off']))

        def Supply(self):
            return self.ENUM_SUPPLY[self.supply]


    class Logging(Element):

        __validLoglevels = ["DEBUG", "ERROR", "INFO"]
        loglevel : int
        __logFile : str
        inverterMinimumVoltage : int
        switchDelaySeconds : int
        floatVoltage : int

        def __init__(self, loglevel : str, logfile : str):

            self.loglevel = self._getByStr(loglevel, self.__validLoglevels)
            self.__logFile = logfile
            self.__logFile = logfile = logfile

    logging : Logging
    approvals : list[Approval]


    def __init__(self, settingsfile : str):
        self.approvals = list()
        tree = ET.parse(settingsfile)
        root = tree.getroot()

        tagLogging = root.find("Logging")
        self.logging = self.Logging(tagLogging.attrib['loglevel'], tagLogging.attrib['file'])
        self.inverterMinimumVoltage = float(root.find("InverterSettings").attrib['minimumVoltage'])
        self.switchDelaySeconds = int(root.find("InverterSettings").attrib['switchDelaySeconds'])
        self.floatVoltage = float(root.find("InverterSettings").attrib['floatVoltage'])

        for app in root.find('Approvals').findall('App'):
            self.approvals.append(self.Approval(app))

    def getApproval(self, name : str):
        for app in self.approvals:
            if app.name == name:
                return app

        return None





    approvals : list()

