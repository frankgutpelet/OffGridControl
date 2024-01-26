import unittest
from Consumer import Consumer, TimeSwitch
from datetime import time, datetime
from Settings import Settings

class ConsumerTest(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
