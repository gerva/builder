import os
import process
import tempfile
import shutil
import process
import log_setup

log = log_setup.logger(__name__)

class GitInterface(object):
    """
    an interface for git.
    It creates a local mirror (git clone --mirror).
    """
    def __init__(self, mirror_directory, remote_repository):
        self.name = remote_repository.rpartition('/')[2]
        self.remote_repository = remote_repository
        self.mirror_directory = os.path.join(mirror_directory, self.name)
        self.working_directory = None
        log.debug('created {0}'.format(self.mirror_directory))

    def update_mirror(self):
        if not os.path.exists(self.mirror_directory):
            try:
                 os.makedirs(self.mirror_directory)
            except OSError, e:
                raise GitError('cannot create mirror directory: {0}'.format(e))
            self.clone_mirror()
        self.fetch()

    def clone_mirror(self):
        """
        clones the remote mirror locally
        """
        cmd = ['git', 'clone', '--mirror', self.remote_repository, self.mirror_directory]
        self.run(cmd, cwd=None, env=None, timeout=None)

    def create_working_directory(self, working_directory):
        log.info('creating working directory: {0}'.format(working_directory))
        cmd = ['git', 'clone', self.mirror_directory, working_directory]
        self.run(cmd, cwd=None, env=None, timeout=None)

    def close(self):
        """
        invoke this method before when you don't need to access
        the git repository anymore. It takes care of cleaning up the disk
        """
        try:
           if os.path.exists(self.working_directory):
               shutil.rmtree(self.working_directory)
        except TypeError, e:
           # working dir is None
           pass

    def fetch(self):
        """
        updates objects and refs in local mirror
        """
        cmd = ['git', 'fetch']
        cwd = self.mirror_directory
        self.run(cmd, cwd, env=None, timeout=None)

    def add_tag(self, tag_name):
        """
        adds a tag
        """
        cmd = ['git', 'tag', tag_name]
        cwd = self.working_directory
        self.run(cmd, cwd, env=None, timeout=None)

    def ls_remote(self, remote):
        """
        returns the output of git ls-remote <remote>
        """
        if remote not in self.get_remotes():
            raise GitError('requested remote does not exist: {0}'.format(remote))
        cmd = ['git', 'ls-remote', remote]
        cwd = self.mirror_directory
        fd = self.run(cmd, cwd, env=None, timeout=None)
        with open(fd.name) as out:
             lines = out.readlines()
        return lines

    def get_remote_tags(self, remote):
        """
        returns a list of remote tags
        """
        tags = [ GitTag(tag) for tag in self.ls_remote(remote) ]
        return [ tag for tag in tags if tag.name is not None ]

    def get_remote_tag_names(self, remote):
        """
        returns a list of tag names
        """
        return [ tag.name for tag in self.get_remote_tags(remote) ]

    def get_remote_branches(self, remote):
        """
        returns a list of remote branches
        """
        branches = [ GitBranch(branch) for branch in self.ls_remote(remote) ]
        return [ branch for branch in branches if branch.name is not None ]

    def get_remote_branch_names(self, remote):
        """
        returns a list of remote branches
        """
        return [ branch.name for branch in self.get_remote_branches(remote) ]

    def get_tracked_branches(self):
        cmd = ['git', 'branch' ]
        cwd = self.mirror_directory
        fd = self.run(cmd, cwd, env=None, timeout=None)
        with open(fd.name) as out:
            lines = out.readlines()
        return [ branch for branch in lines ]

    def get_remotes(self):
        cmd = ['git', 'remote', '-v']
        cwd = self.mirror_directory
        fd = self.run(cmd, cwd, env=None, timeout=None)
        with open(fd.name) as out:
            lines = out.readlines()
        return [ remote.split('\t')[0] for remote in lines if  '(fetch)' in remote ]

    def add_remote(self, name, url):
        """
        a lightweight version of git remote add <options> <name> <url>
        <options> is not supported!
        """
        if name in self.get_remotes():
            raise GitError('cannot add {0}: remote already exists'.format(name))
        cmd = ['git', 'remote', 'add', name, url ]
        cwd = self.mirror_directory
        self.run(cmd, cwd=cwd, env=None, timeout=None)

    def rm_remote(self, name):
        """
        removes a remote from mirror
        """
        if not name in self.get_remotes():
            raise GitError('cannot remove {0}: remote does not exist'.format(name))
        cmd = ['git', 'remote', 'rm', name ]
        cwd = self.mirror_directory
        self.run(cmd, cwd=cwd, env=None, timeout=None)

    def push(self, remote):
        pass

    def push_tag(self, tag_name, remote_name):
        pass

    def create_local_branch(self, branch_name):
        pass

    def git_push_branch(self, branch_name, remote_branch_name, remote):
        pass

    def current_branch(self):
        cmd = ['git', 'branch']
        cwd = self.working_directory
        fd = self.run(cmd, cwd=cwd, env=None, timeout=None)
        with open(fd.name, 'r') as out:
            lines = out.readlines()
        for line in lines:
            if '*' in line:
               return line.partition('*')[2].strip()

    def branch(self, name, start_point):
        cmd = ['git', 'branch', '--track', name, start_point ]
        cwd = self.working_directory
        self.run(cmd, cwd, env=None, timeout=None)

    def checkout(self, name):
        if not os.path.exists(self.working_directory.name):
            raise GitError('checkout branch: working directory does not exist')
        cmd = ['git', 'checkout', name]
        cwd = self.working_directory
        self.run(cmd, cwd, env=None, timeout=None)

    def run(self, cmd, cwd, env, timeout):
        proc = process.ExternalProcess()
        try:
            returncode = proc.execute(cmd, cwd=cwd, env=None, timeout=None)
            if returncode != 0:
                raise GitError('error running: {0}; cwd = {1}; return code = {1}'.format(' '.join(cmd), cwd, returncode))
            std_out = proc.out_fd
            return std_out
        except process.ExternalProcessError, e:
            raise GitError('failed to execute: {0}; cwd = {1}'.format(' '.join(cmd), cwd))

class GitError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class GitTag(object):
    def __init__(self, tag):
        if tag is None:
            return
        self.commitId = None
        self.name = None
        if 'refs/tags' in tag:
            self.commitId, dummy, self.name = tag.strip().partition('refs/tags/')
            self.commitId = self.commitId.strip()

    def __str__(self):
        return '{0}: {1}'.format(self.commitId, self.name)


class GitBranch(object):
    def __init__(self, branch):
        if branch is None:
            return
        self.commitId = None
        self.name = None
        if 'refs/heads' in branch:
            self.commitId, dummy, self.name = branch.strip().partition('refs/heads/')
            self.commitId = self.commitId.strip()

    def __str__(self):
        return '{0}: {1}'.format(self.commitId, self.name)
