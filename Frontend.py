from IFrontend import IFrontend
from IFifo import IFifo
import json

class Frontend(IFrontend):
	transferDataGlobal = {'batv', 'batI', 'solV', 'todayE', 'yesterdayE', 'supply', 'charchingstate'}
	transferDataDevice = {'name', 'state', 'mode', 'ontime'}
	_deviceList: dict
	_globalData : dict
	__fifo : IFifo

	def __init__(self, fifo, logger):
		self.__fifoPath = "/tmp/solarWatcher.fifo"
		self.__logger = logger
		self.__fifo = fifo
		self._deviceList = dict()
		self._globalData = dict()

	def updateDevice(self, transferData : list):
		self.__checkParam(transferData, self.transferDataDevice)

		if "AUTO" == transferData['mode'].upper():
			transferData['state'] += "(AUTO)"
		self._deviceList[transferData['name']] = transferData

	def updateGlobalData(self, transferData : list):
		self.__checkParam(transferData, self.transferDataGlobal)
		self._globalData = transferData

	def sendData(self):
		data = self._globalData
		data['Devices'] = self._deviceList

		self.__logger.Debug("Send data to fifo: " + json.dump(data))
		self.__fifo.open()
		json.dump(data, self.__fifo)
		self.__fifo.close()

	def __checkParam(self, param : list, pattern: list):
		for element in pattern:
			if element in param:
				continue
			self.__logger.Error(element + " not included in argument list: " + str(param))
			raise Exception(element + " not included in argument list: " + str(param))

		for element in param:
			if element in pattern:
				continue
			self.__logger.Error(element + " not included in argument list: " + str(param))
			raise Exception(element + " not included in argument list: " + str(param))





