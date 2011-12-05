import os
import process
import tempfile
import shutil
import process
import log

log = log.logger(__name__)

class GitInterface(object):
    """
    an interface for git.
    It creates a local mirror (git clone --mirror).
    """
    def __init__(self, mirror_directory, remote_repository):
        self.name = remote_repository.rpartition('/')[2]
        self.remote_repository = remote_repository
        self.mirror_directory = os.path.join(mirror_directory, self.name)
        self.working_copy = None
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
        git_clone = process.ExternalProcess()
        returncode = git_clone.execute(cmd, cwd=None, env=None, timeout=None)
        if returncode != 0:
            raise GitError('failed to execute: {0}'.format(' '.join(cmd)))

    def create_working_directory(self):
        pass

    def close(self):
        """
        invoke this method before when you don't need to access
        the git repository anymore. It takes care of cleaning up the disk
        """
        if os.path.exists(self.working_copy):
             shutil.rmtree(self.working_copy)

    def fetch(self):
        """
        updates objects and refs in local mirror
        """
        cmd = ['git', 'fetch']
        cwd = self.mirror_directory
        git_fetch = process.ExternalProcess()
        returncode = git_fetch.execute(cmd, cwd=cwd, env=None, timeout=None)
        if returncode != 0:
            raise GitError('failed to execute: {0}; cwd = {1}; return code = {1}'.format(' '.join(cmd), cwd, returncode))

    def add_tag(self, tag_name):
        pass

    def get_tag_names(self, remote):
        return [ tag.name for tag in self.get_tags(remote) ]

    def get_tags(self, remote):
        """
        returns a list of remote tags
        """
        cmd = ['git', 'ls-remote', remote]
        cwd = self.mirror_directory
        git_ls = process.ExternalProcess()
        returncode = git_ls.execute(cmd, cwd=cwd, env=None, timeout=None)
        if returncode != 0:
            raise GitError('failed to execute: {0}; cwd = {1}; return code = {1}'.format(' '.join(cmd), cwd, returncode))
        with open(git_ls.out_fd.name) as out:
            lines = out.readlines()
        return [ GitTag(tag) for tag in lines ]

    def get_remotes(self):
        cmd = ['git', 'remote', '-v']
        cwd = self.mirror_directory
        git_remote = process.ExternalProcess()
        returncode = git_remote.execute(cmd, cwd=cwd, env=None, timeout=None)
        if returncode != 0:
            raise GitError('failed to execute: {0}; cwd = {1}; return code = {1}'.format(' '.join(cmd), cwd, returncode))
        with open(git_remote.out_fd.name) as out:
            lines = out.readlines()
        return [ remote.split('\t')[0] for remote in lines if  '(fetch)' in remote ]

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


class GitTag(object):
    def __init__(self, tag):
        self.commitId = None
        self.name = None
        if tag is None:
            return
        if 'refs/tags' in tag:
            self.commitId, dummy, self.name = tag.strip().partition('refs/tags/')
            self.commitId = self.commitId.strip()

    def __str__(self):
        return '{0}: {1}'.format(self.commitId, self.name)
