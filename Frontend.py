from IFrontend import IFrontend
from IFifo import IFifo
import json
import traceback
from Daly import Daly

class Frontend(IFrontend):
	transferDataGlobal = {'batV', 'batI', 'solV', 'todayE', 'yesterdayE', 'supply', 'chargingstate'}
	transferDataDevice = {'name', 'state', 'mode', 'ontime'}
	transferDataBMS = {'batV', 'batI', 'soc'}
	_deviceList: dict
	_globalData : dict
	__fifo : IFifo

	def __init__(self, fifo, logger, daly):
		self.__logger = logger
		self.__fifo = fifo
		self._deviceList = dict()
		self._globalData = dict()
		self.bms = daly

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
		self.bms.read()
		data['batV'] = self.bms.getVoltage()
		data['sumI'] = self.bms.getCurrent()
		data['soc'] = self.bms.getSOC()
		data['Devices'] = self._deviceList
		try:
			output = json.dumps(data)
			self.__fifo.open()
			self.__fifo.write(output)
			self.__fifo.close()
		except:
			self.__logger.Error("Failed writing to Fifo" + traceback.format_exc())

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

	def clearDeviceList(self):
		self._deviceList.clear()



