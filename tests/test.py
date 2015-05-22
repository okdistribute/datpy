import unittest
from dat import Dat

class DatTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.dat = Dat()
    cls.dat.init()

  @classmethod
  def tearDownClass(cls):
    cls.dat.clean()

class SimpleTest(DatTest):

  def test_add_with_dataset(self):
    output = self.dat.add("examples/contracts.csv", dataset="contracts")
    self.assertEqual(0, output)
    output = self.dat.export(dataset="contracts")
    self.assertEqual(len(output), 770)

  def test_add_with_abbr_dataset(self):
    output = self.dat.add("examples/contracts.csv", d="contracts2")
    self.assertEqual(0, output)
    output = self.dat.export(dataset="contracts2")
    self.assertEqual(len(output), 770)

  def test_add_file(self):
    output = self.dat.write("examples/blob.txt", d="contracts_file")
    self.assertEqual(0, output)
    output = self.dat.cat("examples/blob.txt", dataset="contracts_file")
    self.assertEqual(output, "hello world\n")

if __name__ == '__main__':
  unittest.main()
