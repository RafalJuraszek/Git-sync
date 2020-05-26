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
    
    def initialize(self, localPath):
        try:
            self.localRepo = Repo(localPath)
            if not self.localRepo.bare:                
                for r in self.localRepo.remotes:
                    print(type(r))
                    print(r)
                    if r.name != 'origin':
                        self.remotes.append(r)
                    else:
                        self.origin = r                
            else:
                log(f'Repo not loaded correctly from {localPath}')
            return self
        except exc.InvalidGitRepositoryError:
            log(f'Invalid git repository in {localPath}')
        return None

    def create(self, origin, localPath):
        Repo.clone_from(origin, localPath)
        return self.initialize(localPath)
    
    def addRemote(self, remoteUrl, remoteName=''):
        try:
            newRemote = self.localRepo.create_remote(remoteName, remoteUrl)        
            self.remotes.append(newRemote)
        except exc.GitCommandError as e:
            log(e.message)


    def addRemotes(self, remotes):
        for remote in remotes:
            self.addRemote(remote, self.generateRemoteName(remote))

    def generateRemoteName(self, remote:str):
        return remote

    def pull(self, branch):
        self.origin.update()
        self.localRepo.git.pull('--rebase')

    def pushToRemotes(self, branch):
        self.localRepo.git.checkout(branch, '--force')
        for remote in self.remotes:
            remote.push('--force')

                # , '--set-upstream', remote.name, branchName
    def synchroAll(self):
        for ref in self.origin.refs:
            print(ref)
            branchName = ref.name.split('/')[1]
            print(branchName)
            if branchName == 'HEAD':
                continue
            # checkout to next branch
            self.localRepo.git.checkout(branchName, '--force')
            self.pull(branchName)
            self.pushToRemotes(branchName)


# repo = Repo('C:\\Users\\Adrian\\Studia\\IoTest')


def synchronize2(syncRepo: SyncRepository):
    syncRepo.synchroAll()

repo = SyncRepository()
# repo.create(r'https://github.com/Roshoy/test/', 'C:\\Users\\Adrian\\Studia\\IoTest')
repo.initialize('C:\\Users\\Adrian\\Studia\\IoTest')
repo.addRemote('https://bitbucket.org/IoTeamRak/test', 'bitbucket')
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