import unittest
import json
try:
  import pandas
except:
  pandas = False

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

  @classmethod
  def tearDownClass(cls):
    cls.local.close()
    cls.local.clean()

class SimpleTest(DatTest):

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
    res = self.dat.to_csv()
    self.assertEqual(type(res), str)

  def test_put(self):
    data = '{"one": "world"}\n{"hello": "mars"}'
    res = self.dat.put_bulk(data)
    self.assertEquals(res.status_code, 200)

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
    data = {
      "hey": "you"
    }
    res = self.dat.put(data)
    self.assertEquals(res['hey'], data['hey'])

    res = self.dat.rows()
    self.assertEquals(type(res), list)

    # test that options are passed correctly
    res = self.dat.rows(opts={"limit": 1})
    self.assertEquals(len(res), 1)

  def test_put_bulk(self):
    with open('examples/contracts.csv') as fp:
      self.assertTrue(len(self.dat.changes()) < 10)
      res = self.dat.put_bulk(fp, format='csv')
      self.assertTrue(len(self.dat.changes()) > 700)


@unittest.skipIf(pandas is False, "skipping pandas tests")
class TestPandas(DatTest):

  def test_pandas(self):
    with open('examples/contracts.csv') as fp:
      res = self.dat.put_bulk(fp, format='csv')
      df = self.dat.to_pandas()
      self.assertEquals(type(df), pandas.core.frame.DataFrame)
      self.assertEquals(df.shape, (770, 12))

      # clean column, turn into float
      df['amtSpent'] = df['amtSpent'].str.replace(r'[$,]', '').astype('float')

      # create ranked column.
      df['amtSpentRank'] = df['amtSpent'].rank()

      self.assertEquals(df.shape, (770, 13))

      res = self.dat.put_pandas(df)
      print res.status_code



if __name__ == '__main__':
  unittest.main()
