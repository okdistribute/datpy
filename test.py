import unittest

from dat import Dat

host = 'http://localhost:6461'

class DatTest(unittest.TestCase):

    def setUp(self):
        self.dat = Dat(host)

    def test_info(self):
        res = self.dat.info()
    	self.assertEqual(res['dat'], 'Hello')

if __name__ == '__main__':
    unittest.main()
