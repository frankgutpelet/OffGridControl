from IVictronReader import IVictronReader
from mylogging import Logging

import traceback
from ICom import ICom

class VictronReader(IVictronReader):

    """this class reads state of the victron energy charger and controls it"""
    coms: list
    mode: str

    class Error:
        No_error = 0
        Battery_voltage_too_high = 2
        Charger_temperature_too_high = 17
        Charger_over_current = 18
        Charger_current_reversed = 19
        Bulk_time_limit_exceeded = 20
        Current_sensor_issue_sensor_bias_sensor_broken = 21
        Terminals_overheated = 26
        Input_voltage_too_high_solar_panel = 33
        Input_current_too_high_solar_panel = 34
        Input_shutdown_due_to_excessive_battery_voltage = 38
        Factory_calibration_data_lost = 116
        Invalid_incompatible_firmware = 117
        User_settings_invalid = 119

        def getError(errorcode):
            if (VictronReader.Error.No_error == errorcode):
                return "No_error"
            elif (VictronReader.Error.Battery_voltage_too_high == errorcode):
                return "Battery_voltage_too_high"
            elif (VictronReader.Error.Charger_temperature_too_high == errorcode):
                return "Charger_temperature_too_high"
            elif (VictronReader.Error.Charger_over_current == errorcode):
                return "Charger_over_current"
            elif (VictronReader.Error.Charger_current_reversed == errorcode):
                return "Charger_current_reversed"
            elif (VictronReader.Error.Bulk_time_limit_exceeded == errorcode):
                return "Bulk_time_limit_exceeded"
            elif (VictronReader.Error.Current_sensor_issue_sensor_bias_sensor_broken == errorcode):
                return "Current_sensor_issue_sensor_bias_sensor_broken"
            elif (VictronReader.Error.Terminals_overheated == errorcode):
                return "Terminals_overheated"
            elif (VictronReader.Error.Input_voltage_too_high_solar_panel == errorcode):
                return "Input_voltage_too_high_solar_panel"
            elif (VictronReader.Error.Input_current_too_high_solar_panel == errorcode):
                return "Input_current_too_high_solar_panel"
            elif (VictronReader.Error.Input_shutdown_due_to_excessive_battery_voltage == errorcode):
                return "Input_shutdown_due_to_excessive_battery_voltage"
            elif (VictronReader.Error.Factory_calibration_data_lost == errorcode):
                return "Factory_calibration_data_lost"
            elif (VictronReader.Error.Invalid_incompatible_firmware == errorcode):
                return "Invalid_incompatible_firmware"
            else:
                return "unknown Error Errorcode: " + str(errorcode)

    class ChargingState:
        Off = 0
        Low_power = 1
        Fault = 2
        Bulk = 3
        Absorption = 4
        Float = 5
        Inverting = 9
        @classmethod
        def GetState(cls, state):
            if VictronReader.ChargingState.Off == state:
                return "Off"
            elif VictronReader.ChargingState.Low_power == state:
                return "Low Power"
            elif VictronReader.ChargingState.Fault == state:
                return "Fault"
            elif VictronReader.ChargingState.Bulk == state:
                return "Bulk"
            elif VictronReader.ChargingState.Absorption == state:
                return "Absorption"
            elif VictronReader.ChargingState.Float == state:
                return "Float"
            elif VictronReader.ChargingState.Inverting == state:
                return "Inverting"
            else:
                return "Unknown state " + str(state)

    def __init__(self, logger : Logging, comports: list):
        self.logger = logger
        self.coms = comports

        for comport in comports:
            comport.connect()


    def getValues(self):
        batV = 0
        batVDiv = 0
        solV = 0
        cur = 0
        mod = 0
        today = 0
        yesterday = 0
        for com in self.coms:
            for i in range(3):
                values = self.__parseVictron(com)
                if values:
                    break
            if not values:
                com.disconnect()
                com.connect()
                values = self.__parseVictron(com)
            if not values:
                self.logger.Error("No Data from Victron Charger " + com.com)
                return None

            if float(values['batV']) > batV:
                batV += values['batV']
                batVDiv += 1
            if float(values['batV']) > solV:
                solV = values['solV']
            cur += values['cur']
            mod = values['mod']
            today += values['today']
            yesterday += values['yesterday']

        if 0 != batVDiv:
            batV = batV / batVDiv
        return {'batV' : batV, 'batI' : cur, 'solV' : solV, 'todayE' : today, 'yesterdayE' : yesterday, 'chargingstate' : self.ChargingState.GetState(mod)}





    def __parseVictron(self, com):

        text = ""
        ret = {'batV': 0, 'solV': 0, 'cur': 0, 'mod': 'unknown', 'today': 0, 'yesterday': 0}
        com.flush()
        control = ""

        for i in range(1, 20):
            line = com.readline()
            line = str(line)

            if 'checksum' in line:
                break
            else:
                text += line

            try:
                pair = line.split('\\r\\n')[0].split('b\'')[1].split('\\t')
            except:
                self.logger.Debug("could not parse: " + line)
                continue

            if 2 > len(pair):
                continue

            if ('V' == pair[0]):
                ret['batV'] = int(pair[1]) / 1000
                if 0 < ret['batV']:
                    control += 'VB '
            elif ('VPV' == pair[0]):
                ret['solV'] = int(pair[1]) / 1000
                if 0 < ret['solV']:
                        control += 'VPV '
            elif ('I' == pair[0]):
                ret['cur'] = int(pair[1]) / 1000
                if  0 <= ret['cur']:
                    control += 'I '
            elif ('CS' == pair[0]):
                ret['mod'] = int(pair[1])
                control += "CS "
            elif ('H20' == pair[0]):
                ret['today'] = int(pair[1])
                control += "H20 "
            elif ('H22' == pair[0]):
                ret['yesterday'] = int(pair[1])
                control += "H22 "
            elif ('ERR' == pair[0]):
                self.errorcode = int(pair[1])
                if (VictronReader.Error.No_error != self.errorcode):
                    self.logger.Error(VictronReader.Error.getError(self.errorcode))
            if ('VB' in control and 'VPV' in control and 'I' in control and 'CS' in control and 'H20' in control and 'H22' in control):
                return ret

        return None
