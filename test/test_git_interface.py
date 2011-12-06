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
        self.remote_name = 'TEST_REMOTE'

    def tearDown(self):
        self.git.close()
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
        # tags
        self.assertTrue('origin' in self.git.get_remotes())
        self.assertTrue('test' in self.git.get_remote_tag_names('origin'))
        self.assertRaises(git.GitError, lambda: self.git.get_remote_tag_names('wrong remote name'))
        # branches
        self.assertTrue('master' in self.git.get_remote_branch_names('origin'))
        self.assertRaises(git.GitError, lambda: self.git.get_remote_branch_names('wrong remote name'))
        # remotes
        self.assertTrue('origin' in self.git.get_remotes())
        self.assertFalse('non exisiting remote' in self.git.get_remotes())
        self.assertRaises(git.GitError, lambda: self.git.add_remote('origin', 'url'))
        self.assertRaises(git.GitError, lambda: self.git.rm_remote('this does not exist'))
        self.git.add_remote(self.remote_name, 'url')
        self.assertTrue(self.remote_name in self.git.get_remotes())
        self.git.rm_remote(self.remote_name)
        self.assertFalse(self.remote_name in self.git.get_remotes())


