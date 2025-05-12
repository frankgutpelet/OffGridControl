import threading
import traceback
import time
from Daly import Daly
import requests
from mylogging import Logging
from Settings import Settings
import time

class SupplySwitch:
    Thread : threading.Thread
    bms : Daly
    isOn : bool
    logger : Logging
    channel = "POWER2"
    timer = 0
    minimumSOC : int
    minimumV : float
    treshold = 0.3
    switchOffDelaySec = 600
    kill = False
    switchDNS = "192.168.178.25"

    def __init__(self, dalyBms, logging, settings : Settings):
        self.bms = dalyBms
        self.isOn = False
        self.logger = logging
        self.Thread = threading.Thread(target=self.__thread, args=())
        self.switchState = 'OFF'
        self.minimumSOC = settings.minimumSoc
        self.minimumV = settings.inverterMinimumVoltage
        self.switchOfftime = 0
        self.Thread.start()

        pass

    def __thread(self):
        self.logger.Debug("start SupplySwitch Thread")

        try:
            while False == self.kill:
                time.sleep(1)
                if 0 != self.switchOfftime:
                    self.switchOfftime -= 1
                    continue

                self.bms.read()
                soc = int(self.bms.getSOC())
                voltage = float(self.bms.getVoltage())
                if (self.minimumSOC > soc): # or (self.minimumV >= voltage): momentan nicht nach spannung weil es schwankt, wenn abgeschaltet wird geladen => spannung steigt
                    self.isOn = False
                elif(self.minimumSOC < soc): # and (self.minimumV + self.treshold <= voltage):
                    self.isOn = True
                self.__switch()
                self.timer += 1
                if (10 <= self.timer):
                    self.__getSwitchState()
                    self.timer = 0

        except:
            self.logger.Error("SupplySwitch Thread crashed. Reason: " + traceback.format_exc())

    def __getSwitchState(self):
        try:
            response = requests.get("http://" + self.switchDNS + "/cm?cmnd=" + self.channel)
        except:
            self.switchState = "OFFLINE"
            self.logger.Error("SuplySwitch is Offline - Solar supply failed")
            return

        if 200 != response.status_code:
            self.logger.Error("no connection to SupplySwitch. Response: " + str(response.status_code))
            return
        self.switchState = response.json()[self.channel]
        self.logger.Debug("SupplySwitch state: " + self.switchState)

    def __switch(self):
        response = None
        if self.isOn:
            if self.switchState == "ON":
                return
            try:
                response = requests.get("http://" + self.switchDNS + "/cm?cmnd=" + self.channel + "%20ON")
            except:
                self.switchState = "OFFLINE"

        else:
            if self.switchState == "OFF":
                return
            self.switchOfftime = self.switchOffDelaySec
            try:
                response = requests.get("http://" + self.switchDNS + "/cm?cmnd=" + self.channel + "%20OFF")
            except:
                self.switchState = "OFFLINE"

        if not response:
            return
        if 200 != response.status_code:
            self.logger.Error("no connection to SupplySwitch. Response: " + str(response.status_code))
            return
        self.switchState = response.json()[self.channel]
