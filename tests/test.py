from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
import os

import datpy

EXAMPLE_DIR = 'examples'

root = os.path.dirname(datpy.__file__)
linkPath = os.path.join(root,EXAMPLE_DIR)
downloadPath = os.path.join(root,'example-download-data')

class DatTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.dat = datpy.Dat()
    if not os.path.exists(downloadPath):
      os.mkdir(downloadPath)

  @classmethod
  def tearDownClass(cls):
    cls.dat.close()
    files = os.listdir(downloadPath)
    for filepath in files:
      os.remove(os.path.join(downloadPath, filepath))
    os.rmdir(downloadPath)

class IOTests(DatTest):

  def test_link_and_download(self):
    link = self.dat.share(linkPath)
    self.assertEquals(len(link), 64)
    self.assertEquals(len(self.dat._opened), 1)
    self.dat.download(link, downloadPath)
    self.assertEquals(os.listdir(downloadPath), os.listdir(linkPath))
    self.assertEquals(len(self.dat._opened), 2)

if __name__ == '__main__':
  unittest.main()
