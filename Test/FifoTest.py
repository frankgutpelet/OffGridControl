import unittest
from FifoWrapper import FifoWrapper

#this unittest only runs on unix OS

class FifoWrapperTest(unittest.TestCase):
    def test_fifo(self):
        fifo = FifoWrapper("tmp")
        fifo.open()
        fifo.write("hello")
        fifo.close()

        file = open("hello", "r")
        str = file.read()
        self.assertEqual("hello", str)
        str = file.read()
        self.assertEqual("", str)


if __name__ == '__main__':
    unittest.main()
