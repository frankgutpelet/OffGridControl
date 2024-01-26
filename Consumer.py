from IConsumer import IConsumer
from xml.etree.ElementTree import Element
from Settings import Settings
from datetime import datetime
from mylogging import Logging
import requests

class TimeSwitch():
    times : list()

    def __init__(self, times : list() ):
        self.times = times

    def isOn(self, now : datetime.time):
        for time in self.times:
            onTime = time.onTime.hour * 60 + time.onTime.minute
            offTime =  time.offTime.hour * 60 + time.offTime.minute
            timestamp = now.hour * 60 + now.minute

            if timestamp > onTime and timestamp < offTime:
                return True
        return False

class Consumer(IConsumer):
    prio : int
    supply : str #Settings.E_SUPPLY
    mode : str # Settings.E_MODE
    name : str
    __dns : str
    timeswitch : TimeSwitch
    isOn : bool
    logger : Logging

    def __init__(self, settings : Element, logger : Logging, timer : list = None):
        self.name = settings.attrib['name']
        self.__dns = settings.attrib['dns']
        self.supply = settings.attrib['supply']
        self.mode = settings.attrib['mode']
        self.prio = settings.attrib['prio']
        self.logger = logger
        if timer:
            self.timeswitch = TimeSwitch(timer)
        else:
            self.timeswitch = None
        self.isOn = False

    def approve(self):
        if self.timeswitch:
            self.isOn = self.timeswitch.isOn(datetime.now().time())
        else:
            self.isOn = True


    def prohibit(self):
        self.isOn = False

    def push(self):
        if self.isOn:
            cmd = "on"
        else:
            cmd = "off"
        try:
            response = requests.get(self.__dns + "/cm?cmnd=Power%20" + cmd)
        except Exception:
            self.logger.Error("No connection to " + self.name + "(DNS: " + self.__dns + ")")
