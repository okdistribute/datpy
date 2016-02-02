from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
import os

import datpy

EXAMPLE_DIR = 'examples'

root = os.path.dirname(datpy.__file__)
linkPath = os.path.join(root,EXAMPLE_DIR)
downloadDir = os.path.join(os.path.join(root,'example-download-data'))

class DatTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    if not os.path.exists(downloadDir):
      os.makedirs(downloadDir)
    cls.downloadPath = os.path.join(downloadDir, EXAMPLE_DIR)
    cls.dat = datpy.Dat()

  @classmethod
  def tearDownClass(cls):
    cls.dat.close()
    files = os.listdir(cls.downloadPath)
    for filepath in files:
      os.remove(os.path.join(cls.downloadPath,filepath))
    os.rmdir(cls.downloadPath)
    os.rmdir(downloadDir)

class IOTests(DatTest):

  def test_link_and_download(self):
    link = self.dat.link(linkPath)
    self.assertTrue(link.startswith('dat://'))
    self.assertEquals(len(link.replace('dat://', '')), 64)
    self.assertEquals(len(self.dat._opened), 1)
    self.dat.download(link, path=self.downloadPath)
    self.assertEquals(os.listdir(self.downloadPath), os.listdir(linkPath))
    self.assertEquals(len(self.dat._opened), 2)

if __name__ == '__main__':
  unittest.main()
