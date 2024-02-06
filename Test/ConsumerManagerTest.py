import unittest
from ConsumerManager import ConsumerManager
from IInverter import IInverter
from LoggerStub import LoggerStub
from IConsumer import IConsumer

class InverterMock(IInverter):

    def __init__(self):
        self.data = {'batV': 25, 'batI': 5, 'solV': 60, 'todayE': 0, 'yesterdayE': 0, 'supply': 'Solar',
                     'charchingstate': 'float'}
        pass

    def getChargerData(self):
        return self.data

class ConsumerMock(IConsumer):
    prio : int
    isOn = False
    pushed = False
    on = 0
    mode = "On"
    minTime = 0

    def __init__(self,  prio : int):
        self.prio = prio
        pass

    def approve(self):
        ret = not self.isOn
        self.isOn = True
        return ret

    def prohibit(self):
        ret = not self.isOn
        self.isOn = False
        return ret

    def push(self):
        self.pushed = True

    def onTime(self):
        return  self.on

class SettingsMock():
    inverterMinimumVoltage=24
    floatVoltage=28
    switchDelaySeconds=60




class ConsumerManagerTest(unittest.TestCase):

    def test_GivenConsumerListWithSeveralPrios_WhenUpdateConsumers_ThenSortByPrio(self):
        inverter = InverterMock()
        logger = LoggerStub()
        settings = SettingsMock
        manager = ConsumerManager(inverter,logger,settings)
        consumers = [ConsumerMock(5), ConsumerMock(3), ConsumerMock(7)]

        manager.updateConsumerList(consumers)

        self.assertEqual(3, manager.consumers[0].prio)
        self.assertEqual(5, manager.consumers[1].prio)
        self.assertEqual(7, manager.consumers[2].prio)

    def test_GivenConsumerStateOnInverterUtility_WhenManageApprovals_SwitchOnAndPush(self):
        inverter = InverterMock()
        logger = LoggerStub()
        settings = SettingsMock
        manager = ConsumerManager(inverter, logger, settings)
        consumers = [ConsumerMock(1)]

        manager.updateConsumerList(consumers)
        manager.manageApprovals()

        self.assertTrue(consumers[0].isOn)
        self.assertTrue(consumers[0].pushed)

    def test_GivenConsumerStateOnInverterUtilityStateOn_WhenManageApprovals_SwitchOnAndDontPush(self):
        inverter = InverterMock()
        logger = LoggerStub()
        settings = SettingsMock
        manager = ConsumerManager(inverter, logger, settings)
        consumers = [ConsumerMock(1)]
        consumers[0].isOn = True

        manager.updateConsumerList(consumers)
        manager.manageApprovals()

        self.assertTrue(consumers[0].isOn)
        self.assertFalse(consumers[0].pushed)

    def test_GivenConsumerStateOffInverterUtility_WhenManageApprovals_SwitchOffAndDontPush(self):
        inverter = InverterMock()
        logger = LoggerStub()
        settings = SettingsMock
        manager = ConsumerManager(inverter, logger, settings)
        consumers = [ConsumerMock(1)]
        consumers[0].mode = "Off"

        manager.updateConsumerList(consumers)
        manager.manageApprovals()

        self.assertFalse(consumers[0].isOn)
        self.assertFalse(consumers[0].pushed)

    def test_GivenConsumerStateOffInverterUtilityStateOn_WhenManageApprovals_SwitchOffAndPush(self):
        inverter = InverterMock()
        logger = LoggerStub()
        settings = SettingsMock
        manager = ConsumerManager(inverter, logger, settings)
        consumers = [ConsumerMock(1)]
        consumers[0].isOn = True
        consumers[0].mode = "Off"

        manager.updateConsumerList(consumers)
        manager.manageApprovals()

        self.assertFalse(consumers[0].isOn)
        self.assertTrue(consumers[0].pushed)

    def test_GivenWellSwitchedConsumer_WhenPush_ThenPushConsumer(self):
        inverter = InverterMock()
        logger = LoggerStub()
        settings = SettingsMock
        manager = ConsumerManager(inverter, logger, settings)
        consumers = [ConsumerMock(1)]
        consumers[0].isOn = True
        consumers[0].mode = "Off"

        manager.updateConsumerList(consumers)
        manager.push()

        self.assertTrue(consumers[0].pushed)

    def test_GivenConsumerAutoSurplus_WhenUtilityMode_ThenSwitchOff(self):
        inverter = InverterMock()
        logger = LoggerStub()
        settings = SettingsMock
        manager = ConsumerManager(inverter, logger, settings)
        consumers = [ConsumerMock(1)]
        consumers[0].isOn = True
        consumers[0].mode = "Auto"
        consumers[0].supply = "Surplus"
        inverter.data['supply'] = "Utility"

        manager.updateConsumerList(consumers)
        manager.manageApprovals()

        self.assertFalse(consumers[0].isOn)
        self.assertTrue(consumers[0].pushed)

    def test_GivenConsumerAutoSurplus_WhenBatteryMode_ThenSwitchOff(self):
        inverter = InverterMock()
        logger = LoggerStub()
        settings = SettingsMock
        manager = ConsumerManager(inverter, logger, settings)
        consumers = [ConsumerMock(1)]
        consumers[0].isOn = True
        consumers[0].mode = "Auto"
        consumers[0].supply = "Surplus"
        inverter.data['supply'] = "Solar"
        inverter.data['batI'] = 0

        manager.updateConsumerList(consumers)
        manager.manageApprovals()

        self.assertFalse(consumers[0].isOn)
        self.assertTrue(consumers[0].pushed)

    def test_GivenConsumerAutoSurplus_WhenSolarMode_ThenSwitchOff(self):
        inverter = InverterMock()
        logger = LoggerStub()
        settings = SettingsMock
        manager = ConsumerManager(inverter, logger, settings)
        consumers = [ConsumerMock(1)]
        consumers[0].isOn = True
        consumers[0].mode = "Auto"
        consumers[0].supply = "Surplus"
        inverter.data['supply'] = "Solar"

        manager.updateConsumerList(consumers)
        manager.manageApprovals()

        self.assertFalse(consumers[0].isOn)
        self.assertTrue(consumers[0].pushed)

    def test_GivenConsumerAutoSurplus_WhenSurplusMode_ThenSwitchOn(self):
        inverter = InverterMock()
        logger = LoggerStub()
        settings = SettingsMock
        manager = ConsumerManager(inverter, logger, settings)
        consumers = [ConsumerMock(1)]
        consumers[0].isOn = False
        consumers[0].mode = "Auto"
        consumers[0].supply = "Surplus"
        inverter.data['supply'] = "Solar"
        inverter.data['batV'] = 29

        manager.updateConsumerList(consumers)
        manager.manageApprovals()

        self.assertTrue(consumers[0].isOn)
        self.assertTrue(consumers[0].pushed)



if __name__ == '__main__':
    unittest.main()
