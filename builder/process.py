import sys
import os
import subprocess
import tempfile
import datetime
import log
log = log.logger(__name__)

class ExternalProcess(object):
   """
   a wrapper for subprocess
   """
   def __init__(self):
       # logging
       self.out_fd = None
       self.err_fd = None
       self.stdout_r = None
       self.stderr_r = None
       # command
       self.proc = None
       self.cmd = None
       self.cwd = None
       self.env = None
       self.timeout = None
       # enable log?
       self.log_enable = True

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

   def _set_cmd(self, cmd):
       if not isinstance(cmd, list):
           raise TypeError('cmd is not a list')
       self.cmd = cmd

   def _set_cwd(self, cwd):
       try:
           if not os.path.exists(cwd):
               msg = 'not existing cwd ({0})'.format(cwd)
               raise ExternalProcessError(msg)
       except TypeError, e:
         if cwd is not None:
             log.debug('cwd error: expected string')
             raise
       self.cwd = cwd

   def _set_env(self, env):
       if not isinstance(env, dict) and env is not None:
           raise TypeError('env is not a dictionary')
       self.env = env

   def _set_timeout(self, timeout):
       if not isinstance(timeout, (int, float)) and timeout is not None:
           raise TypeError('timeout should be None, int or float')
       try:
           self.timeout = datetime.datetime.now() + datetime.timedelta(0,timeout)
       except TypeError:
           self.timeout = None

   def sanitise_input(self, cmd, cwd, env, timeout):
       # cmd, cwd, env and timeout need to be reset
       # before executing a new comand
       self.cmd = None
       self.cwd = None
       self.env = None
       self.timeout = None
       # check cmd is a list
       self._set_cmd(cmd)
       # ensuring working directory exists or is None
       self._set_cwd(cwd)
       # check env is a dict
       self._set_env(env)
       # check timeout
       self._set_timeout(timeout)
       log.debug('executing:')
       log.debug('cmd: {0}'.format(' '.join(self.cmd)))
       log.debug('cwd: {0}'.format(self.cwd))
       log.debug('env: {0}'.format(self.env))
       log.debug('timeout: {0}'.format(self.timeout))

   def execute(self, cmd, cwd, env, timeout):
       self.sanitise_input(cmd, cwd, env, timeout)
       self.reset_files()
       self.proc = subprocess.Popen(self.cmd, cwd=self.cwd, env=self.env,
                               stdout = self.out_fd,
                               stderr = self.err_fd)
       self.wait_completion_or_timeout()
       # log all remaining lines from out and err files
       self.log_last_lines()
       return self.proc.returncode

   def log_last_lines(self):
       if self.log_enable:
           out_file_read = open(self.out_fd.name, 'r')
           for line in out_file_read.readlines() :
               log.debug(line.strip())
           err_file_read = open(self.err_fd.name, 'r')
           for line in err_file_read.readlines() :
               log.error(line.strip())

   def got_timeout(self):
       if self.timeout == None:
           return False
       return datetime.datetime.now() >= self.timeout

   def wait_completion_or_timeout(self):
       while self.proc.poll() is None:
           self.write_process_out_to_log()
           if self.timeout is not None:
              if self.got_timeout():
                  log.debug('timeout: terminating the process')
                  log.debug('now: {0}, timeout {1}'.format(datetime.datetime.now(), self.timeout ))
                  self.proc.terminate()
       log.debug('exit code: {0}'.format(self.proc.returncode))
       return self.proc.returncode

   def write_process_out_to_log(self):
       if self.timeout is not None:
           now = datetime.datetime.now()
           diff = self.timeout < now
           #print 't - now = {0} - {1} = {2}'.format(self.timeout, datetime.datetime.now(), diff)
       if not self.log_enable:
           stdout = self.stdout_r.readline().rstrip()
           if stdout != '':
               log.debug('stdout: {0}'.format(stdout))
       stderr = self.stderr_r.readline().rstrip()
       if stderr != '':
           log.debug('stderr: {0}'.format(stderr))

class ExternalProcessError(Exception):
   def __init__(self, value):
       self.value = value

   def __str__(self):
       return repr(self.value)
