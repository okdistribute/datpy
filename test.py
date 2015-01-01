import unittest

from dat import LocalDat, Dat, DatServerError

host = 'http://localhost:6461'

class DatTest(unittest.TestCase):
  """
  Basic tests assuming the dat is already set up and listening on port 6461.

  For more advanced testing, we will want to (at some point) instantiate the
  Dat ourselves.
  """

  @classmethod
  def setUpClass(cls):
    cls.local = LocalDat()
    cls.local.init()
    cls.local.listen()
    cls.dat = Dat(host)

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
    self.assertEqual(type(res), str)

  def test_put(self):
    data = {
      "hello": "world"
    }
    res = self.dat.put(data)
    self.assertEquals(res['hello'], data['hello'])
    self.assertTrue('key' in res)

    ## raises conflict
    data = {
      "key": res['key'],
      "hello": "world"
    }
    self.assertRaises(DatServerError, self.dat.put, data)

  def test_rows(self):
    res = self.dat.rows()
    self.assertEquals(type(res), list)
    res = self.dat.rows(opts={"limit": 1})

  @classmethod
  def tearDownClass(cls):
    cls.local.close()
    cls.local.clean()

if __name__ == '__main__':
  unittest.main()
