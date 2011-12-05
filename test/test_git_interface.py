import os
import sys
import tempfile
import unittest
import shutil
import builder.git_interface as git

class testGitInterface(unittest.TestCase):
    """
    test class for executor module
    """
    def setUp(self):
        self.mirror_dir = tempfile.mkdtemp()
        print self.mirror_dir
        self.git = git.GitInterface(self.mirror_dir, sys.path[0])

    def tearDown(self):
        shutil.rmtree(self.mirror_dir)

    def testMirrorFromLocal(self):
        """
        testing a mirror clone 
        """
        self.git.update_mirror()
        self.assertEqual(os.path.exists(self.mirror_dir), True)
