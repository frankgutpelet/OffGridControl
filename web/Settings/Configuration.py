import xml.etree.ElementTree as ET

class Configuration(object):
    def __init__(self):
        self.configfile = ET.parse("../../OffgridControl/Settings.xml")
        self.root = self.configfile.getroot()


    def setMode(self, device, mode):
        device = device.split(' [')[0]
        for child in self.root:
            if 'name' in child.attrib and device == child.attrib['name']:
                child.attrib['mode'] = mode
                self.configfile.write("../Releases.xml", xml_declaration=True, encoding="UTF-8")
                return


