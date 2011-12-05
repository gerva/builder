import unittest
import builder.process as ex
import os

class testExternalProcess(unittest.TestCase):
    """
    test class for executor module
    """
    def setUp(self):
        self.e = ex.ExternalProcess()
        self.e.log_enable = False

    def testSimpleExecute(self):
        """
        testing a simple command
        """
        cmd_1 = [ 'cd', '..' ]
        cmd_2 = [ 'ls', 'A_]1msn1iisn a' ]
        cmd_3 = [ 'sleep', '1' ]
        self.assertEqual(self.e.execute(cmd_1, cwd=os.path.join('/'), env=None, timeout=None), 0)
        self.assertEqual(self.e.execute(cmd_2, cwd=os.path.join('/'), env=None, timeout=None), 1)
        self.assertEqual(self.e.execute(cmd_1, cwd=None, env=None, timeout=None), 0)
        self.assertEqual(self.e.execute(cmd_1, cwd=None, env={'MY_VAR': '/tmp'}, timeout=None), 0)
        self.assertEqual(self.e.execute(cmd_1, cwd=None, env={'MY_VAR': '/tmp'}, timeout=2), 0)
        self.assertEqual(self.e.execute(cmd_3, cwd=None, env={'MY_VAR': '/tmp'}, timeout=None), 0)
        self.assertNotEqual(self.e.execute(cmd_3, cwd=None, env={'MY_VAR': '/tmp'}, timeout=0.2), 0)

    def testBadInputForExecute(self):
        """
        passing to the executor, wrong commands
        """
        # excute... None
        self.assertRaises(TypeError, lambda: self.e.execute(None, cwd=None, env=None, timeout=None))
        # wrong cmd type (cmd expects a list)
        self.assertRaises(TypeError, lambda: self.e.execute(cmd='ls', cwd=None, env=None, timeout=None))
        self.assertRaises(TypeError, lambda: self.e.execute(cmd=1, cwd='aaaa', env=None, timeout=None))
        self.assertRaises(TypeError, lambda: self.e.execute(None, cwd='aaaa', env=None, timeout=None))
        # cwd should be a string... passing a list
        self.assertRaises(TypeError, lambda: self.e.execute(cmd=['ls'], cwd=['/nonexisitingdir'], env=None, timeout=None))
        # cwd does not exist
        self.assertRaises(ex.ExternalProcessError, lambda: self.e.execute(cmd=['ls'], cwd='/nonexisitingdir', env=None, timeout=None))
        # env
        self.assertRaises(TypeError, lambda: self.e.execute(['cd'], cwd=None, env=list(), timeout=None))
        self.assertRaises(TypeError, lambda: self.e.execute(['cd'], cwd=None, env=1, timeout=None))
        self.assertRaises(TypeError, lambda: self.e.execute(['cd'], cwd=None, env='', timeout=None))
        # timeout
        self.assertRaises(TypeError, lambda: self.e.execute(['cd'], cwd=None, env='', timeout=''))

