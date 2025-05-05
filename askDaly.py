import Daly
from Com import TTYWrapper

class LoggerStub:
    def __init__(self):
        pass

    def Debug(self, msg):
        print(msg)

    def Error(self, msg):
        print(msg)

logger = LoggerStub()


com = TTYWrapper('/dev/ttyUSB1', 9600, logger)
while(True):
	daly = Daly.Daly(com, logger)
	daly.read()
	print(daly.getSOC())





#print(daly.getVoltage() + daly.getSOC())

