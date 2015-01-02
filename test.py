import unittest
import json
try:
  import pandas as pd
  import numpy as np
except:
  pd = False
  np = False

from dat import LocalDat, DatAPI, DatServerError


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
    cls.dat = DatAPI(host)

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

  def test_to_json(self):
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

    # test that to_json works the same
    res = self.dat.to_json(opts={"limit": 1})
    self.assertEquals(len(res), 1)

  def test_put_bulk(self):
    with open('examples/contracts.csv') as fp:
      self.assertTrue(len(self.dat.changes()) < 10)
      res = self.dat.put_bulk(fp, format='csv')
      self.assertTrue(len(self.dat.changes()) > 700)


@unittest.skipIf(pd is False, "skipping pandas tests")
class TestPandas(DatTest):

  def test_pandas(self):
    with open('examples/contracts.csv') as fp:
      res = self.dat.put_bulk(fp, format='csv')
      df = self.dat.to_pandas()
      self.assertEquals(type(df), pd.core.frame.DataFrame)
      self.assertEquals(df.shape, (770, 12))

      # clean column, turn into float
      df['amtSpent'] = df['amtSpent'].str.replace(r'[$,]', '').astype('float')

      # create ranked column.
      df['amtSpentRank'] = df['amtSpent'].rank()
      self.assertEquals(df.shape, (770, 13))

      # okay, put it in dat
      res = self.dat.put_pandas(df)
      self.assertEquals(res.status_code, 200)

      # get the new data in a data frame. we should see the new column there.
      df_with_rank = self.dat.to_pandas()
      self.assertEquals(df_with_rank.shape, (770, 13))
      self.assertTrue(df_with_rank['amtSpentRank'].equals(df['amtSpentRank']))

      # also, all of the new data should be at version 2
      version_two = pd.Series(np.array([2] * 770))
      self.assertTrue(df_with_rank['version'].equals(version_two))
      self.assertFalse(df_with_rank['version'].equals(df['version']))



if __name__ == '__main__':
  unittest.main()
