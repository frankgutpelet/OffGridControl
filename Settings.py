import xml.etree.ElementTree as ET
from datetime import time
from xml.dom import minidom
import copy

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
        soc : int
        def __init__(self, onTime : str, offTime : str, soc : str):
            self.soc = int(soc)
            self.onTime = time(int(onTime.split(':')[0]), int(onTime.split(':')[1]))
            self.offTime = time(int(offTime.split(':')[0]), int(offTime.split(':')[1]))


    class Approval(Element):

        name : str
        dns : str
        prio : int
        supply : str
        soc : int
        mode : str
        timers : list
        minTimeRunningMinutes : int

        def __init__(self, config : ET.Element):
            self.name = config.attrib['name']
            self.dns = config.attrib['dns']
            self.prio = int(config.attrib['prio'])
            self.supply = self._getByStr(config.attrib['supply'], Settings.E_SUPPLY.names)
            self.mode = self._getByStr(config.attrib['mode'], Settings.E_MODE.names)
            if 'soc' in config.attrib:
                self.soc = int(config.attrib['soc'])
            else:
                self.soc = 0
            if ('minTimeRunningMinutes' in config.attrib):
                self.minTimeRunningMinutes = config.attrib['minTimeRunningMinutes']
            else:
                self.minTimeRunningMinutes = 0
            self.timers = list()
            for timerConfig in config.findall('Timer'):
                self.timers.append(Settings.Timer(timerConfig.attrib['on'], timerConfig.attrib['off'], timerConfig.attrib['soc']))

        def Supply(self):
            return self.ENUM_SUPPLY[self.supply]

        def addTag(self, parent):
            config = ET.SubElement(parent, "App")
            config.attrib['name'] = self.name
            config.attrib['dns'] = self.dns
            config.attrib['prio'] = str(self.prio)
            config.attrib['supply'] = self.supply
            config.attrib['mode'] = self.mode
            config.attrib['soc'] = str(self.soc)
            if self.minTimeRunningMinutes != 0:
                config.attrib['minTimeRunningMinutes'] = str(self.minTimeRunningMinutes)
            for timer in self.timers:
                timElem = ET.Element("Timer")
                timElem.attrib['soc'] = str(timer.soc)
                timElem.attrib['on'] = f"{timer.onTime.hour:02}" + ":" +  f"{timer.onTime.minute:02}"
                timElem.attrib['off'] = f"{timer.offTime.hour:02}" + ":" +  f"{timer.offTime.minute:02}"
                config.append(timElem)
            return config


    class Logging(Element):

        __validLoglevels = ["DEBUG", "ERROR", "INFO"]
        loglevel : int
        logFile : str
        inverterMinimumVoltage : int
        switchDelaySeconds : int
        floatVoltage : int

        def __init__(self, loglevel : str, logfile : str):

            self.loglevel = self._getByStr(loglevel, self.__validLoglevels)
            self.logFile = logfile

    logging : Logging
    approvals : list[Approval]
    updated = False
    inverterMinimumVoltage : float
    minimumSoc : int
    inverterMinimumPowerW : int

    def __init__(self, settingsfile : str):
        self.approvals = list()
        self.filename = settingsfile
        tree = ET.parse(settingsfile)
        root = tree.getroot()

        tagLogging = root.find("Logging")
        self.logging = self.Logging(tagLogging.attrib['loglevel'], tagLogging.attrib['file'])
        self.inverterMinimumVoltage = float(root.find("InverterSettings").attrib['minimumVoltage'])
        self.minimumSoc = int(root.find("InverterSettings").attrib['minimumSOC'])
        self.inverterMinimumPowerW = int(root.find("InverterSettings").attrib['inverterMinimumPowerW'])
        self.switchDelaySeconds = int(root.find("InverterSettings").attrib['switchDelaySeconds'])
        self.floatVoltage = float(root.find("InverterSettings").attrib['floatVoltage'])

        for app in root.find('Approvals').findall('App'):
            self.approvals.append(self.Approval(app))

    def getApproval(self, name : str):
        for app in self.approvals:
            if app.name == name:
                return copy.deepcopy(app)

        return None

    def changeApproval(self, name, newApp : Approval):
        for app in self.approvals:
            if app.name == name:
                if app != newApp:
                    app.mode = newApp.mode
                    self.updated = True

    def save(self):
        if not self.updated:
            return
        root = ET.Element("Settings")
        InverterSettings = ET.SubElement(root, "InverterSettings")
        InverterSettings.attrib["minimumVoltage"] = str(self.inverterMinimumVoltage)
        InverterSettings.attrib["floatVoltage"] = str(self.floatVoltage)
        InverterSettings.attrib["switchDelaySeconds"] = str(self.switchDelaySeconds)
        InverterSettings.attrib["minimumSOC"] = str(self.minimumSoc)
        InverterSettings.attrib["inverterMinimumPowerW"] = str(self.inverterMinimumPowerW)
        Logging = ET.SubElement(root, "Logging")
        Logging.attrib["loglevel"] = self.logging.loglevel
        Logging.attrib["file"] = self.logging.logFile
        Approvals = ET.SubElement(root, "Approvals")
        for app in self.approvals:
            app.addTag(Approvals)
        string = minidom.parseString(ET.tostring(root))

        output = open(self.filename, "w")
        output.write(string.toprettyxml(indent="  "))
        output.close()

    approvals : list()

