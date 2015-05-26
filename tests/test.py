import unittest
from dat import Dat

try:
  import pandas as pd
except:
  pd = False

class DatTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.dat = Dat()
    cls.dat.init()

  @classmethod
  def tearDownClass(cls):
    cls.dat.clean()

class SimpleTest(DatTest):

  def test_insert_with_dataset(self):
    version = self.dat.import_file("examples/contracts.csv", dataset="contracts")
    self.assertEqual(len(version), 64)
    output = self.dat.export(dataset="contracts")
    self.assertEqual(len(output), 770)

  def test_insert_with_abbr_dataset(self):
    version = self.dat.import_file("examples/contracts.csv", d="contracts2")
    self.assertEqual(len(version), 64)
    output = self.dat.export(dataset="contracts2")
    self.assertEqual(len(output), 770)

  def test_write_file(self):
    version = self.dat.write_file("examples/blob.txt", dataset="blob_txt")
    self.assertEqual(len(version), 64)
    output = self.dat.cat("examples/blob.txt", dataset="blob_txt")
    self.assertEqual(output, "hello world\n")

  def test_write_blob_from_python(self):
    version = self.dat.write("helloworld.txt", "hello world", dataset="hello_world_blob")
    self.assertEqual(len(version), 64)
    output = self.dat.cat("helloworld.txt", dataset="hello_world_blob")
    self.assertEqual(output, "hello world")

@unittest.skipIf(pd is False, "skipping pandas tests")
class TestPandas(DatTest):

  def test_pandas(self):
    # clean column, turn into float
    df = pd.read_csv('examples/contracts.csv')
    self.assertEquals(df.shape, (770, 10))

    df['amtSpent'] = df['amtSpent'].str.replace(r'[$,]', '')

    # insert data
    version = self.dat.import_dataframe(df, d="pandas")
    self.assertEqual(64, len(version))

    output = self.dat.export(dataset="pandas")
    self.assertEqual(len(output), 770)

    df = self.dat.export_as_dataframe(dataset="pandas")

    # modify a column
    # create ranked column.
    df['amtSpentRank'] = df['amtSpent'].rank()
    self.assertEquals(df.shape, (770, 13))

    # okay, put it back in dat
    version = self.dat.add_from_pandas(df, d="pandas", key="key")
    self.assertEqual(len(version), 64)

    # and get it back out
    output = self.dat.export(dataset="pandas")
    self.assertEqual(len(output), 770)
    df_with_rank = pd.DataFrame.from_dict(output)

    # get the new data in a data frame.
    # we should see the updated data and new column there.
    self.assertEquals(df_with_rank.shape, (770, 13))

    # do some type conversion
    # TODO: save dtypes and automagically parse them for the python user
    # if coming to/from pandas
    df_with_rank['amtSpentRank'] = df_with_rank['amtSpentRank'].astype('float')

    self.assertTrue(df_with_rank['amtSpentRank'].equals(df['amtSpentRank']))

if __name__ == '__main__':
  unittest.main()
