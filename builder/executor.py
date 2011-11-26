import sys
import os
import subprocess
import tempfile

class Executor(object):
   """
   a wrapper for subprocess
   """
   def __init__(self):
       # 
       self.out_fd = None 
       self.err_fd = None 
       self.stdout_r = None 
       self.stderr_r = None 

   def __del__(self):
       # closing open files (if any)
       if self.stdout_r:
           self.stdout_r.close()
       if self.stderr_r:
           self.stderr_r.close()

   def reset_files(self):
       if self.stdout_r:
           self.stdout_r.close()
       if self.stderr_r:
           self.stderr_r.close()
       self.out_fd = tempfile.NamedTemporaryFile()
       self.err_fd = tempfile.NamedTemporaryFile()
       self.stdout_r = open(self.out_fd.name, 'r')
       self.stderr_r = open(self.err_fd.name, 'r')

   def execute(self, cmd, cwd, env, timeout):
       # check cmd is a list
       if not isinstance(cmd, list):
           raise TypeError('cmd is not a list')
       # ensuring working directory exists
       try:
           if not os.path.exists(cwd):
               msg = 'not existing cwd ({0})'.format(cwd)
               raise ExecutorError(msg)
       except TypeError, e:
         if cwd is not None:
             print 'cwd error: expected string'
             raise 
       self.reset_files()
       proc = subprocess.Popen(cmd, cwd=cwd, env=env, 
                               stdout = self.out_fd,
                               stderr = self.err_fd)
       proc.wait()
       return proc.returncode 
   
class ExecutorError(Exception):
   def __init__(self, value):
       self.value = value

   def __str__(self):
       return repr(self.value)
