import unittest
from ConsumerManager import ConsumerManager
from IInverter import IInverter
from LoggerStub import LoggerStub
from IConsumer import IConsumer

class InverterMock(IInverter):
    def __init__(self):
        pass

    def getChargerData(self):
        return {'batV' : 25, 'batI' : 5, 'solV' : 60, 'todayE' : 0, 'yesterdayE' : 0, 'supply' : 'Solar', 'charchingstate' : 'float'}

class ConsumerMock(IConsumer):
    prio : int
    isOn = False
    pushed = False
    onTime = 0
    mode = "On"

    def __init__(self,  prio : int):
        self.prio = prio
        pass

    def approve(self):
        ret = not self.isOn
        self.isOn = True
        return ret

    def prohibit(self):
        pass

    def push(self):
        self.pushed = True

    def onTime(self):
        return  self.onTime

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




if __name__ == '__main__':
    unittest.main()
