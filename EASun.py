from IEASun import IEASun
import threading
import time
import RPi.GPIO as GPIO
import traceback

#runs only under UNIX

class EASun(IEASun):
    gpioPin = 4

    def __init__(self, logger):
        self.__solarSupply = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.ReadThread = threading.Thread(target=self.__ReadThread, args=())
        self.logger = logger
        self.ReadThread.start()

    def IsRunning(self):
        if self.ReadThread.isAlive():
            return True
        else:
            return False

    def getMode(self):
        if self.__solarSupply:
            return "Solar"
        return "Utility"


    def __ReadThread(self):
        self.logger.Debug("start SupplyStatus Thread")
        debounceCnt = 0
        try:
            while True:
                try:

                    # wait for 2 seconds for falling edge (sample 100ms)
                    if None != GPIO.wait_for_edge(self.gpioPin, GPIO.FALLING, timeout=2000):
                        if 1 == GPIO.input(self.gpioPin):  # debounce
                            continue
                        # self.logger.Debug("Wait for falling edge")
                        self.__solarSupply = True
                        debounceCnt = 0
                    else:
                        # no falling edge - indicator does not blink anymore
                        debounceCnt += 1
                        if 5 == debounceCnt:
                            self.__solarSupply = False
                except Exception as e:
                    self.logger.Error("SolarSupply: " + str(e))
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setup(self.gpioPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        except:
            self.logger.Error("SupplyStatus Thread crashed. Reason: " + traceback.format_exc())
