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
            if 0 == offTime:
                offTime = 24 * 60
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
    logger : Logging
    timestampOn : int
    requests : bool

    def __init__(self, settings : Settings.Approval, logger : Logging):
        self.name = settings.name
        self.__dns = settings.dns
        self.supply = settings.supply
        self.mode = settings.mode
        self.prio = settings.prio
        self.logger = logger
        self.timestampOn = 0
        self.minTime = int(settings.minTimeRunningMinutes)
        self.requests = True

        if  0 < len(settings.timers):
            self.timeswitch = TimeSwitch(settings.timers)
        else:
            self.timeswitch = None

        self.isOn = False
        if 'On' == self.mode:
            self.isOn = True


    def approve(self):
        if not 'Auto' == self.mode:
            return self.isOn
        if self.timeswitch:
            self.isOn = self.timeswitch.isOn(datetime.now().time())
        else:
            if not self.isOn:
                self.timestampOn = datetime.now().timestamp()
            self.isOn = True

        return self.isOn


    def prohibit(self):
        ret = self.isOn
        if 'Auto' == self.mode:
            self.isOn = False
        return ret

    def push(self):
        if self.isOn:
            cmd = "on"
        else:
            cmd = "off"
        try:
            if self.requests:
                self.logger.Debug("send command to " + self.__dns + ": " + cmd)
                response = requests.get(self.__dns + "/cm?cmnd=Power%20" + cmd)
                if 200 == response.status_code:
                    self.isOn = not self.isOn
                else:
                    self.isOn = not self.isOn
        except Exception:
            self.logger.Error("No connection to " + self.name + "(DNS: " + self.__dns + ")")



    def onTime(self):
        return datetime.now().timestamp() - self.timestampOn
