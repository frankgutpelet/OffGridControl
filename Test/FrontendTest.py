import unittest
from Frontend import Frontend
from IFifo import IFifo

class FrontendTest(unittest.TestCase):
    class FifoMock(IFifo):
        msg : str
        isopen : bool

        def __init__(self, filepath: str):
            self.isopen = False
            self.msg = str()
            pass

        def open(self):
            self.isopen = True

        def close(self):
            self.isopen = False

        def write(self, message: str):
            self.msg += message

    class LoggerStub:
        error = ""
        def Debug(self, msg):
            pass
        def Error(self, msg):
            self.error = msg


    def test_GivenDeviceUpdated_WhenSendData_ThenWriteFifo(self):
        fifo = self.FifoMock('')
        logger = self.LoggerStub()
        deviceInfo = {'name' : 'Device1', 'state' : 'On', 'mode' : 'On', 'ontime' : '60'}
        frontend = Frontend(fifo, logger)
        frontend.updateDevice(deviceInfo)
        frontend.sendData()
        self.assertEqual('{"Devices": {"Device1": {"name": "Device1", "state": "On", "mode": "On", "ontime": "60"}}}', fifo.msg)

    def test_GivenGlobalDataUpdated_WhenSendData_ThenWriteFifo(self):
        fifo = self.FifoMock('')
        logger = self.LoggerStub()
        globalData = {'batv' : '20', 'batI' : '5', 'solV' : '50', 'todayE': '5000', 'yesterdayE' : '45000', 'supply' : 'solar', 'charchingstate' : 'float'}
        frontend = Frontend(fifo, logger)
        frontend.updateGlobalData(globalData)
        frontend.sendData()
        self.assertEqual('{"batv": "20", "batI": "5", "solV": "50", "todayE": "5000", "yesterdayE": "45000", "supply": "solar", "charchingstate": "float", "Devices": {}}', fifo.msg)

    def test_GivenGlobalDataAndDevicesUpdated_WhenSendData_ThenWriteFifo(self):
        fifo = self.FifoMock('')
        logger = self.LoggerStub()
        globalData = {'batv' : '20', 'batI' : '5', 'solV' : '50', 'todayE': '5000', 'yesterdayE' : '45000', 'supply' : 'solar', 'charchingstate' : 'float'}
        frontend = Frontend(fifo, logger)
        frontend.updateGlobalData(globalData)

        deviceInfo = {'name': 'Device1', 'state': 'On', 'mode': 'On', 'ontime': '60'}
        frontend.updateDevice(deviceInfo)
        deviceInfo = {'name': 'Device2', 'state': 'Off', 'mode': 'Auto', 'ontime': '60'}
        frontend.updateDevice(deviceInfo)

        frontend.sendData()
        self.assertEqual('{"batv": "20", "batI": "5", "solV": "50", "todayE": "5000", "yesterdayE": "45000", "supply": "solar", "charchingstate": "float", "Devices": {"Device1": {"name": "Device1", "state": "On", "mode": "On", "ontime": "60"}, "Device2": {"name": "Device2", "state": "Off(AUTO)", "mode": "Auto", "ontime": "60"}}}', fifo.msg)

    def test_GivenwrongDeviceUpdateParameterlist_WhenUpdateDevice_ThenException(self):
        fifo = self.FifoMock('')
        logger = self.LoggerStub()
        deviceInfo = {'Name' : 'Device1', 'state' : 'On', 'mode' : 'On', 'ontime' : '60'}
        frontend = Frontend(fifo, logger)
        try:
            frontend.updateDevice(deviceInfo)
        except:
            self.assertTrue(True)
            return
        self.assertFalse(True)

    def test_GivenUncompleteGlobalParameterlist_WhenUpdateGlobalData_ThenException(self):
        fifo = self.FifoMock('')
        logger = self.LoggerStub()
        globalData = {'batI' : '5', 'solV' : '50', 'todayE': '5000', 'yesterdayE' : '45000', 'supply' : 'solar', 'charchingstate' : 'float'}
        frontend = Frontend(fifo, logger)
        try:
            frontend.updateGlobalData(globalData)
        except:
            self.assertTrue(True)
            return
        self.assertFalse(True)

    def test_GivenAdditionalDataGlobalParameterlist_WhenUpdateGlobalData_ThenException(self):
        fifo = self.FifoMock('')
        logger = self.LoggerStub()
        globalData = {'batv' : '20', 'batI' : '5', 'solV' : '50', 'todayE': '5000', 'yesterdayE' : '45000', 'supply' : 'solar', 'charchingstate' : 'float', 'Das' : 'darf nicht drin sein'}
        frontend = Frontend(fifo, logger)
        try:
            frontend.updateGlobalData(globalData)
        except:
            self.assertTrue(True)
            return
        self.assertFalse(True)