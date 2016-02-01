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

  def tearDownClass(cls):
    cls.dat.close()
    os.rmdir(path)

class IOTests(DatTest):

  def test_link(self):
    self.link = self.dat.link('examples')
    self.assertTrue(link.startswith('dat://'))
    self.assertEquals(len(link.replace('dat://')), 64)
    self.assertEquals(len(dat._opened), 1)

  def test_download(self):
    self.dat.download(self.link, path)
    self.assertEquals(os.listdir(path), os.listdir('examples'))
    self.assertEquals(len(dat._opened), 2)

if __name__ == '__main__':
  unittest.main()
