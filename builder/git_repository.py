import git_interface
import log_setup

log = log_setup.logger(__name__)

class GitRepository(git_interface.GitInterface):
   def __init__(self, mirror_directory, remote_repository):
       git_interface.GitInterface.__init__(self, mirror_directory, remote_repository)
       self.working_directory = None

   def update(self):
       log.info('updating mirror')
       self.update_mirror()

   def create_working_copy(self, working_directory, branch='master'):
       log.info('creating working copy')
       if not branch in self.get_remote_branch_names('origin'):
           raise GitRepositoryError('requested branch {0} does not exists'.format(branch))
       self.working_directory = working_directory
       try:
           self.create_working_directory(self.working_directory)
       except git_interface.GitError, e:
           raise GitRepositoryError('error creating the working directory: {0}'.format(e))

class GitRepositoryError(Exception):
   def __init__(self, value):
       self.value = value

   def __str__(self):
       return repr(self.value)
