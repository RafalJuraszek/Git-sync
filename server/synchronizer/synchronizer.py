import os
from git import Repo
from git import RemoteProgress
from git import exc
from git import Git


repos = ['https://gitlab.com/RafalJuraszek/io-test']

repo = Repo('C:\\Users\\Adrian\\Studia\\IoTest')
print([r for r in repo.remotes])

def synchronize():

    # Repo object used to programmatically interact with Git repositories
    #jesli plik ten jest w repo gita to bierze to repo (brak argumentu), mozna dac sciezke do folderu z gitem
    repo = Repo('C:\\Users\\rafal\\Desktop\\semestr 6\\io\\test')
    # check that the repository loaded correctly
    if not repo.bare:

        origin = repo.remotes['origin']
        print(type(origin))
        origin.pull()
        for i, url_repo in enumerate(repos):
            # najpeirw trzeba stworzyc (ale to bysmy pewnie brali z arajki
            repo1 = repo.create_remote('v1repo{}'.format(i), url_repo)
            #repo1 = repo.remote(name='v1repo{}'.format(i))

            repo1.push()


    else:
        pass

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
            self.origin = repo.remotes['origin']
            self.remotes = [r for r in repo.remotes.items() if r is not self.origin]
            return self
        except exc.InvalidGitRepositoryError:
            log(f'Invalid git repository in {localPath}')            

    def create(self, origin, localPath):
        Git(localPath).clone(origin)
        self.initialize(localPath)
    
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