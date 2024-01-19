import unittest
from Settings import Settings


class SettimgsTest(unittest.TestCase):
    def test_settingsfile(self):
        settings = Settings("Settings.xml")
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
