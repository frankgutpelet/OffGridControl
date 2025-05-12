import logging
import traceback
from Com import TTYWrapper
import struct

class Daly:
    soc = {
            "total_voltage" : 0,
            "current" : 0,
            "soc_percent" : 0}
    logger : logging
    comport : TTYWrapper
    requestSOC = bytes([0xA5, 0x90, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0xFF, 0xFD])
    def __init__(self, tty, logger):
        self.connected = False
        self.logger = logger
        self.comport = tty
        self.logger.Debug("connect to " + self.comport.com)
        if not self.comport.connect():
            self.logger.Error(traceback.format_exc())
            self.logger.Error("Daly - No connection to daly BMS")

    def read(self):
        self.comport.write(self._format_message(90))
        response = self.comport.read(13)
        if len(response) == 13 and response[0] == 0xA5 and response[2] == 0x90:
            parts = struct.unpack('>h h h h', response[4:-1])
            self.soc = {
                "total_voltage": parts[0] / 10,
                # "x_voltage": parts[1] / 10, # always 0
                "current": (parts[2] - 30000) / 10,  # negative=charging, positive=discharging
                "soc_percent": parts[3] / 10
            }
        else:
            self.soc = {
                "total_voltage": 0,
                "current": 0,
                "soc_percent": 0
            }

            return

    def _format_message(self, command, extra=""):
        """
        Takes the command ID and formats a request message

        :param command: Command ID ("90" - "98")
        :return: Request message as bytes
        """
        # 95 -> a58095080000000000000000c2
        message = "a5%i0%s08%s" % (4, command, extra)
        message = message.ljust(24, "0")
        message_bytes = bytearray.fromhex(message)
        message_bytes += self._calc_crc(message_bytes)
        return message_bytes

    def _calc_crc(self, message_bytes):
        """
        Calculate the checksum of a message

        :param message_bytes: Bytes for which the checksum should get calculated
        :return: Checksum as bytes
        """
        return bytes([sum(message_bytes) & 0xFF])

    def getVoltage(self):
        return self.soc['total_voltage']
    def getCurrent(self):
        return self.soc['current']
    def getSOC(self):
        return self.soc["soc_percent"]