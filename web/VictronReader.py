import threading, traceback
import time
import json, sys
import logging

import socket



class VictronReader:
    __instance = None
    batteries = list()

    def GetInstance():
        if (VictronReader.__instance == None):
            return VictronReader()
        return VictronReader.__instance

    def __init__(self):
        if VictronReader.__instance != None:
            raise Exception("This class is a singleton")
        else:
            VictronReader.__instance = self

        self.batV = 0
        self.solV = 0
        self.batI = 0
        self.temp = 0
        self.today = 0
        self.yesterday = 0
        self.supply = "unknown"
        self.chargemode = "unknown"
        self.devices = list()
        self.VictronThread = threading.Thread(target=self.ReadVictronValues, args=())
        self.VictronThread.start()

    def ReadVictronValues(self):
        path = "/tmp/solarWatcher.fifo"
        values = []
        self.batV = 0

        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', 23456))
                    while True:
                        s.listen()
                        conn, addr = s.accept()
                        with conn:
                            try:
                                data = ""
                                while True:
                                    data += conn.recv(2048).decode()
                                    if "" != data:
                                        break
                                logging.error("read full data")
                                self._parseJson(data)
                            except:
                                logging.error(traceback.format_exc() + data)
                                conn.close()
                                s.close()
            except:
                logging.error(traceback.format_exc())
                continue

    def _parseJson(self, data):
        try:
           #{"todayE": 501, "yesterdayE": 728, "batI": 54.6, "solV": 61.02, "batV": 27.975, "supply": "Solar","charchingstate": 4,
            values = json.loads(data)
            self.batV = str(round(float(values['batV']),1))
            self.batI = str(round(float(values['batI']),1))
            self.solV = str(round(float(values['solV']),1))
            self.supply = values['supply']
            self.temp = "0"
            self.today = float(values['todayE'])/100.0
            self.yesterday = float(values['yesterdayE'])/100.0
            self.chargemode = values['chargingstate']


            self.devices.clear()

            for device in values['Devices']:
                self.devices.append(values['Devices'][device])

            logging.error("parsed full data")
        except:
            logging.error(traceback.format_exc() + data)



