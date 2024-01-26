import unittest
from Consumer import Consumer, TimeSwitch
from datetime import time, datetime
from Settings import Settings
from LoggerStub import LoggerStub
class ConsumerTest(unittest.TestCase):


#Test für TimeSwitch

    def test_GivenBeforeTime_WhenAskIsOn_ThenFalse(self):
        timer = Settings.Timer("4:00", "5:00")
        timer = TimeSwitch([timer])
        now = datetime(1900,1,1,3,0)

        self.assertFalse(timer.isOn(now))

    def test_GivenMinuteBeforeTime_WhenAskIsOn_ThenFalse(self):
        timer = Settings.Timer("4:00", "5:00")
        timer = TimeSwitch([timer])
        now = datetime(1900,1,1,3,59)

        self.assertFalse(timer.isOn(now))

    def test_GivenMaxBeforeTime_WhenAskIsOn_ThenFalse(self):
        timer = Settings.Timer("4:00", "5:00")
        timer = TimeSwitch([timer])
        now = datetime(1900,1,1,0,0)

        self.assertFalse(timer.isOn(now))

    def test_GivenAfterTime_WhenAskIsOn_ThenFalse(self):
        timer = Settings.Timer("4:00", "5:00")
        timer = TimeSwitch([timer])
        now = datetime(1900, 1, 1, 6, 0)

        self.assertFalse(timer.isOn(now))

    def test_GivenMinuteAfterTime_WhenAskIsOn_ThenFalse(self):
        timer = Settings.Timer("4:00", "5:00")
        timer = TimeSwitch([timer])
        now = datetime(1900, 1, 1, 5, 1)

        self.assertFalse(timer.isOn(now))

    def test_GivenMaxAfterTime_WhenAskIsOn_ThenFalse(self):
        timer = Settings.Timer("4:00", "5:00")
        timer = TimeSwitch([timer])
        now = datetime(1900, 1, 1, 23, 59)

        self.assertFalse(timer.isOn(now))

    def test_GivenMiddleInTime_WhenAskIsOn_ThenTrue(self):
        timer = Settings.Timer("4:00", "5:00")
        timer = TimeSwitch([timer])
        now = datetime(1900, 1, 1, 4, 30)

        self.assertTrue(timer.isOn(now))

    def test_GivenMinInTime_WhenAskIsOn_ThenTrue(self):
        timer = Settings.Timer("4:00", "5:00")
        timer = TimeSwitch([timer])
        now = datetime(1900, 1, 1, 4, 1)

        self.assertTrue(timer.isOn(now))

    def test_GivenMaxInTime_WhenAskIsOn_ThenTrue(self):
        timer = Settings.Timer("4:00", "5:00")
        timer = TimeSwitch([timer])
        now = datetime(1900, 1, 1, 4, 59)

        self.assertTrue(timer.isOn(now))

#Test für Consumer

    def test_GivenConsumerConfigOn_WhenAprove_ReturnTrue(self):
        settings = Settings("ConsumerTestSettings.xml")
        logger = LoggerStub()
        consumer = Consumer(settings.approvals[0], logger)

        self.assertTrue(consumer.approve())

    def test_GivenConsumerConfigOff_WhenAprove_ReturnFalse(self):
        settings = Settings("ConsumerTestSettings.xml")
        logger = LoggerStub()
        consumer = Consumer(settings.approvals[1], logger)

        self.assertFalse(consumer.approve())

    def test_GivenConsumerConfigOn_WhenProhibit_ReturnTrue(self):
        settings = Settings("ConsumerTestSettings.xml")
        logger = LoggerStub()
        consumer = Consumer(settings.approvals[0], logger)

        self.assertTrue(consumer.prohibit())


    def test_GivenConsumerConfigOnTimeOff_WhenAprove_ReturnTrue(self):
        settings = Settings("ConsumerTestSettings.xml")
        logger = LoggerStub()
        consumer = Consumer(settings.approvals[2], logger)

        self.assertTrue(consumer.approve())

    def test_GivenConsumerConfigOnTimeOn_WhenAprove_ReturnTrue(self):
        settings = Settings("ConsumerTestSettings.xml")
        logger = LoggerStub()
        consumer = Consumer(settings.approvals[3], logger)

        self.assertTrue(consumer.approve())

    def test_GivenConsumerConfigAuto_WhenAprove_ReturnTrue(self):

        settings = Settings("ConsumerTestSettings.xml")
        logger = LoggerStub()
        consumer = Consumer(settings.approvals[4], logger)

        self.assertTrue(consumer.approve())

    def test_GivenConsumerConfigAuto_WhenProhibit_ReturnFalse(self):

        settings = Settings("ConsumerTestSettings.xml")
        logger = LoggerStub()
        consumer = Consumer(settings.approvals[4], logger)

        self.assertFalse(consumer.prohibit())

    def test_GivenConsumerConfigAutoTimeOff_WhenAprove_ReturnFalse(self):

        settings = Settings("ConsumerTestSettings.xml")
        logger = LoggerStub()
        consumer = Consumer(settings.approvals[5], logger)

        self.assertTrue(consumer.approve())

    def test_GivenConsumerConfigAutoTimeOn_WhenAprove_ReturnTrue(self):

        settings = Settings("ConsumerTestSettings.xml")
        logger = LoggerStub()
        consumer = Consumer(settings.approvals[6], logger)

        self.assertTrue(consumer.approve())

if __name__ == '__main__':
    unittest.main()
