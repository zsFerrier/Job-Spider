# -*- coding:utf-8 -*-
import os
import shutil
import unittest
from src.main.python.util.io.FileUtil import FileUtil

class FileUtil1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print "setUpClass..."

    @classmethod
    def tearDownClass(cls):
        print "tearDownClass..."

    def test_getLogConfigPath(self):
        path = FileUtil().getLogConfigPath()
        print path

    def test_getResoursePath(self):
        path = FileUtil().getResoursePath()
        print path


if __name__=="__main__":
    unittest.main()