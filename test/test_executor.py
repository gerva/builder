import unittest
import builder.executor as ex
import os

class testExecutor(unittest.TestCase):
    """
    test class for executor module
    """
    def setUp(self):
        self.e = ex.Executor()
        self.e.log_enable = False

    def testSimpleExecute(self):
        """
        testing a simple command
        """
        cmd_1 = [ 'cd', '..' ]
        cmd_2 = [ 'ls', 'A_]1msn1iisn a' ]
        self.assertEqual(self.e.execute(cmd_1, cwd=os.path.join('/'), env=None, timeout=None), 0)
        self.assertEqual(self.e.execute(cmd_2, cwd=os.path.join('/'), env=None, timeout=None), 1)
        self.assertEqual(self.e.execute(['ls'], cwd=None, env=None, timeout=None), 0)

    def testBadInputForExecute(self):
        """
        passing to the executor, wrong commands
        """
        self.assertRaises(TypeError, lambda: self.e.execute(None, cwd=None, env=None, timeout=None))
        self.assertRaises(TypeError, lambda: self.e.execute(cmd='ls', cwd=None, env=None, timeout=None))
        self.assertRaises(TypeError, lambda: self.e.execute(cmd=['ls'], cwd=['/nonexisitingdir'], env=None, timeout=None))
        self.assertRaises(ex.ExecutorError, lambda: self.e.execute(cmd=['ls'], cwd='/nonexisitingdir', env=None, timeout=None))
        self.assertRaises(TypeError, lambda: self.e.execute(cmd=1, cwd='aaaa', env=None, timeout=None))
        self.assertRaises(TypeError, lambda: self.e.execute(None, cwd='aaaa', env=None, timeout=None))
        self.assertRaises(ex.ExecutorError, lambda: self.e.execute(['cd'], cwd='aaaa', env=None, timeout=None))

