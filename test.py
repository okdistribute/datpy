import unittest

from dat import Dat

host = 'http://localhost:6461'

class DatTest(unittest.TestCase):
    """
    Basic tests assuming the dat is already set up and listening on port 6461.

    For more advanced testing, we will want to (at some point) instantiate the
    Dat ourselves.
    """

    def setUp(self):
        self.dat = Dat(host)

    def test_info(self):
        res = self.dat.info()
    	self.assertEqual(res['dat'], 'Hello')

    def test_changes(self):
        res = self.dat.changes()
        self.assertEqual(type(res), list)

    def test_session(self):
        res = self.dat.session()
        self.assertEqual(res['loggedOut'], True)

    def test_csv(self):
        res = self.dat.csv()


if __name__ == '__main__':
    unittest.main()
