import unittest
from datpy.dat import LocalDat

class DatTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.local = LocalDat()
    cls.local.init()

  @classmethod
  def tearDownClass(cls):
    cls.local.clean()

class SimpleTest(DatTest):

  def test_add(self):
    output = self.local.add("examples/contracts.csv")
    self.assertEqual(0, output)

  def test_cat(self):
    output = self.local.cat()
    self.assertEqual(770, len(output))
      	
  def test_heads(self):
    output = self.local.heads()
    self.assertEqual(str, type(output))
    self.assertTrue(len(output)  > 20)
  
if __name__ == '__main__':
  unittest.main()
