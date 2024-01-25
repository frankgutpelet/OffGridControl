import unittest
from VictronReader import VictronReader
from ICom import ICom
from IEASun import IEASun
testdata=   ["b'PID\\t0xA057\r\n",
                "b'FW\\t159\r\n",
                "b'SER#\\tHQ2302CFVEQ\r\n",
                "b'V\\t28610\r\n",
                "b'I\\t7300\r\n",
                "b'VPV\\t64650\r\n",
                "b'PPV\\t218\r\n",
                "b'CS\\t4\r\n",
                "b'MPPT\\t1\r\n",
                "b'OR\\t0x00000000\r\n",
                "b'ERR\\t0\r\n",
                "b'LOAD\\tON\r\n",
                "b'H19\\t8301\r\n",
                "b'H20\\t95\r\n",
                "b'H21\\t584\r\n",
                "b'H22\\t73\r\n",
                "b'H23\\t465\r\n",
                "b'HSDS\\t97\r\n",
                "b'Checksum\\t0"]

class comMock(ICom):
    testdataIterator : int
    def __init__(self, com: str, baud: int):
        self.com = com
        self.baud = baud
        self.testdataIterator = 0
        self.connected = False
        self.data = list(testdata)

    def flush(self):
        pass

    def readline(self):
        self.testdataIterator += 1
        if len(self.data) <= self.testdataIterator:
            self.testdataIterator = 0

        return self.data[self.testdataIterator]

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def isOpen(self):
        return self.connected


class LogStub():
    def Debug(self):
        pass
    def Error(self):
        pass


class VictronReaderTest(unittest.TestCase):

    def test_GivenOneComport_WhenInstance_ThenConnect(self):
        com = comMock("",0)
        logger = LogStub
        reader = VictronReader(logger, [com])
        self.assertTrue(com.connected)

    def test_GivenOneComport_WhenGetValues_ThenValuesFromString(self):
        com = comMock("",0)
        logger = LogStub
        reader = VictronReader(logger, [com])
        data = reader.getValues()
        self.assertEqual(data['batV'], 28.61)
        self.assertEqual(data['batI'], 7.3)

    def test_GivenTwoeComports_WhenGetValues_ThenAddCharchingCurrent(self):
        com1 = comMock("",0)
        com2 = comMock("", 0)
        logger = LogStub
        reader = VictronReader(logger, [com1, com2])
        data = reader.getValues()
        self.assertEqual(data['batI'], 14.6)

    def test_GivenUncompleteData_WhenGetValues_ThenGetNone(self):
        com = comMock("",0)
        com.data[3] = ""
        logger = LogStub
        reader = VictronReader(logger, [com])
        data = reader.getValues()
        self.assertIsNone(data)

    def test_GivenThirdData_WhenGetValues_ThenValuesFromString(self):
        com = comMock("",0)
        logger = LogStub
        com.testdataIterator = 7
        reader = VictronReader(logger, [com])
        data = reader.getValues()
        self.assertEqual(data['batV'], 28.61)
        self.assertEqual(data['batI'], 7.3)

    def test_GivenHalfData_WhenGetValues_ThenValuesFromString(self):
        com = comMock("",0)
        logger = LogStub
        com.testdataIterator = 15
        reader = VictronReader(logger, [com])
        data = reader.getValues()
        self.assertEqual(data['batV'], 28.61)
        self.assertEqual(data['batI'], 7.3)

if __name__ == '__main__':
    unittest.main()
