import os
import shutil
import tempfile
import log_setup
import git_interface as git
import builder.process as process


class Project(object):
   log = log_setup.logger(__name__)
    """
    describes a Project
    """
    def __init__(self, name, git_interface):
        self.name = name
        self.git = git_interface
        self.working_dir = tempfile.mkdtemp()
    
    def checkout(self, branch):
        """
        creates a working copy
        """
        try:
            self.git.update_mirror()
            self.git.create_working_directory(self.working_dir)
            self.git.branch(branch, 'origin/{0}'.format(branch))
        except git.GitError, e:
            raise ProjectError('checkout failed: {0}'.format(e))

    def build(self, cmd, env):
        build = process.ExternalProcess()
        return build.execute(cmd=cmd, cwd=self.working_dir, env=env, timeout=None)
    
    def tag(self, tag_name):
        """
        adds a tag in git
        """
        pass

    def notify(self):
        """
        sends out notifications
        """
        pass

    def copy_working_dir_to(self, path):
        """
        creates a copy of the working dir; 
        working dir is destroyed at the end of the process
        create a copy if you want to preserve the working copy
        """ 
        pass

    def close(self):
        if os.path.exists(self.working_dir):
            shutil.rmtree(self.working_dir)

class ProjectError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
