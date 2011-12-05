import os
import process
import tempfile
import shutil
import process

class GitInterface(object):
    """
    an interface for git.
    It creates a local mirror (git clone --mirror). 
    """
    def __init__(self, mirror_directory, remote_repository):
        self.name = remote_repository.rpartition('/')[2]
        self.remote_repository = remote_repository
        self.mirror_directory = mirror_directory
        self.working_copy = None

    def update_mirror(self):
        if not os.path.exists(self.mirror_directory):
            try: 
                os.mkdirs(os.path.dirname(self.mirror_directory))
            except error, e:
                raise GitError('cannot create mirror directory: {0}'.format(e))
        self.clone_mirror()
        self.fetch()

    def clone_mirror(self):
        """
        clones the remote mirror locally
        """
        cmd = ['git', 'clone', '--mirror', self.remote_repository]
        cwd = self.mirror_directory
        git_clone = process.ExternalProcess()
        returncode = git_clone.execute(cmd, cwd=cwd, env=None, timeout=None)
        if returncode != 0: 
            raise GitError('failed to execute: {0}'.format(' '.join(cmd)))

    def get_mirrors_dir(self):
        return self.mirrors_dir.split(self.repository_name)[0]

    def create_mirrors_dir(self):
        os.makedirs(self.get_mirrors_dir())

    def create_working_directory(self):
        pass

    def close(self):
        pass

    def fetch(self):
        """
        updates objects and refs in local mirror 
        """
        cmd = ['git', 'fetch'] 
        cwd = self.mirror_directory
        git_fetch = process.ExternalProcess()
        returncode = git_fetch.execute(cmd, cwd=cwd, env=None, timeout=None)
        if returncode != 0: 
            raise GitError('failed to execute: {0}; return code = {1}'.format(' '.join(cmd), returncode))

    def get_mirrors_dir(self):
        pass

    def add_tag(self, tag_name):
        pass

    def get_tags(self):
        pass

    def get_branches(self):
        pass

    def push(self, remote):
        pass

    def push_tag(self, tag_name, remote_name):
        pass

    def create_local_branch(self, branch_name):
        pass

    def git_push_branch(self, branch_name, remote_branch_name, remote):
        pass 

class GitError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
