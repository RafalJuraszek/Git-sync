import os
from git import Repo
from git import RemoteProgress
from git import exc
from git import Git


def log(message, lvl = 0):
    print(message)


class SyncRepository:
    def __init__(self):
        self.localRepo = None
        self.origin = None
        self.remotes = []
    
    def initialize(self, local_path):
        try:
            self.localRepo = Repo(local_path)
            if not self.localRepo.bare:                
                for r in self.localRepo.remotes:
                    print(type(r))
                    print(r)
                    if r.name != 'origin':
                        self.remotes.append(r)
                    else:
                        self.origin = r                
            else:
                log(f'Repo not loaded correctly from {local_path}')
            return self
        except exc.InvalidGitRepositoryError:
            log(f'Invalid git repository in {local_path}')
        return None

    def create(self, origin, local_path):
        Repo.clone_from(origin, local_path)
        return self.initialize(local_path)
    
    def add_remote(self, remote_url, remote_name=''):
        try:
            new_remote = self.localRepo.create_remote(remote_name, remote_url)
            self.remotes.append(new_remote)
        except exc.GitCommandError as e:
            log(e)

    def add_remotes(self, remotes):
        for remote in remotes:
            self.add_remote(remote, self.generate_remote_name(remote))

    def generate_remote_name(self, remote:str):
        return remote

    def pull(self, branch):
        self.localRepo.git.pull('--rebase')
        self.localRepo.git.submodule('update', '--recursive')

    def push_to_remotes(self, branch):
        self.localRepo.git.checkout(branch, '--force')
        for remote in self.remotes:
            remote.push('--force')

    def synchronize_all(self):
        for ref in self.origin.refs:
            print(ref)
            branch_name = ref.name.split('/')[1]
            print(branch_name)
            if branch_name == 'HEAD':
                continue
            # checkout to next branch
            self.localRepo.git.checkout(branch_name, '--force')
            self.pull(branch_name)
            self.push_to_remotes(branch_name)


# repo = Repo('C:\\Users\\Adrian\\Studia\\IoTest')


def synchronize2(sync_repo: SyncRepository):
    sync_repo.synchronize_all()


repo = SyncRepository()
# repo.create(r'https://github.com/Roshoy/test/', 'C:\\Users\\Adrian\\Studia\\IoTest')
repo.initialize('C:\\Users\\Adrian\\Studia\\IoTest')
repo.add_remote('https://bitbucket.org/IoTeamRak/test', 'bitbucket')
# repo.initialize('C:\\Users\\Adrian\\Studia\\IoTest')

# remote_refs = repo.remote().refs
# # for remote in repo.remotes:

# remote_refs = repo.remotes['origin'].refs
# print(repo.active_branch)
# repo.git.checkout('synchro')
# print(repo.active_branch)

# for refs in remote_refs:
#     branchName = refs.name.split('/')[1]
#     print(branchName)
#     if branchName == 'HEAD':
#         continue
#     print(refs)
#     refs.checkout()
#     print(repo.active_branch)

synchronize2(repo)