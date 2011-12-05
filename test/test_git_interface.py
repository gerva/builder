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
        self.git = git.GitInterface(self.mirror_dir, sys.path[0])

    def tearDown(self):
        shutil.rmtree(self.mirror_dir)

    def testGitTag(self):
        tag = git.GitTag('2510022b75a5d1ceaf977d3d86431b6bbd4d0a1e	refs/tags/test')
        self.assertEqual(tag.commitId, '2510022b75a5d1ceaf977d3d86431b6bbd4d0a1e')
        self.assertEqual(tag.name, 'test')

    def testMirrorFromLocal(self):
        """
        testing a mirror clone
        """
        self.git.update_mirror()
        self.assertEqual(os.path.exists(self.mirror_dir), True)
        self.assertTrue('test' in self.git.get_tag_names('origin'))
        self.assertTrue('origin' in self.git.get_remotes())

