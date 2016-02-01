from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
import os

import datpy

try:
  import pandas as pd
except:
  pd = False

path = 'example-download-data'

class DatTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.dat = datpy.Dat()

  @classmethod
  def tearDownClass(cls):
    cls.dat.close()
    files = os.listdir(path + '/examples')
    for filepath in files:
      os.remove(path + '/examples/' + filepath)
    os.rmdir(path + '/examples')

class IOTests(DatTest):

  def test_link_and_download(self):
    link = self.dat.link('examples')
    self.assertTrue(link.startswith('dat://'))
    self.assertEquals(len(link.replace('dat://', '')), 64)
    self.assertEquals(len(self.dat._opened), 1)
    self.dat.download(link, path)
    self.assertEquals(os.listdir(path + '/examples'), os.listdir('examples'))
    self.assertEquals(len(self.dat._opened), 2)

if __name__ == '__main__':
  unittest.main()
