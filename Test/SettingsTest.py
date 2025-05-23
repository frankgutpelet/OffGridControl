import unittest
import os
from Settings import Settings


class SettimgsTest(unittest.TestCase):

    def test_GivenLoglevelDebug_WhenInitialize_ThenLoglevelDebug(self):
        settings = Settings("Settings.xml")
        self.assertEqual("DEBUG", settings.logging.loglevel)

    def test_GivenApproval1_WhenInitialize_ThenDNSSolarfreigabe1(self):
        settings = Settings("Settings.xml")
        self.assertEqual("solarfreigabe1", settings.getApproval("approval1").dns)

    def test_GivenApproval1_WhenInitialize_ThenPrio5(self):
        settings = Settings("Settings.xml")
        self.assertEqual(5, settings.approvals[0].prio)

    def test_GivenApproval1_WhenInitialize_ThenSupplySolar(self):
        settings = Settings("Settings.xml")
        self.assertEqual("Solar", settings.getApproval("approval1").supply)

    def test_GivenApproval2_WhenInitialize_ThenStateAuto(self):
        settings = Settings("Settings.xml")
        self.assertEqual("Auto", settings.getApproval("approval2").mode)

    def test_GivenApproval1_WhenInitialize_ThenDNSSolarfreigabe2(self):
        settings = Settings("Settings.xml")
        self.assertEqual("solarfreigabe2", settings.getApproval("approval2").dns)

    def test_GivenApproval2_WhenInitialize_ThenPrio5(self):
        settings = Settings("Settings.xml")
        self.assertEqual(3, settings.getApproval("approval2").prio)

    def test_GivenApproval2_WhenInitialize_ThenSupplySolar(self):
        settings = Settings("Settings.xml")
        self.assertEqual("Utility", settings.getApproval("approval2").supply)

    def test_GivenApproval2_WhenInitialize_ThenStateAuto(self):
        settings = Settings("Settings.xml")
        self.assertEqual("On", settings.getApproval("approval2").mode)

    def test_GivenApproval2_WhenInitialize_ThenTimerOn7h(self):
        settings = Settings("Settings.xml")
        self.assertEqual(7 , settings.getApproval('approval2').timers[0].onTime.hour)

    def test_GivenInizializedWithConfig_WhenSaveConfig_ThenTimestampChanges(self):
        configfile = "Settings.xml"
        timestamp = os.stat(configfile).st_mtime
        settings = Settings(configfile)
        newApp = settings.approvals[0]
        settings.updated = True
        settings.save()
        self.assertNotEqual(timestamp, os.stat(configfile).st_mtime)






if __name__ == '__main__':
    unittest.main()
