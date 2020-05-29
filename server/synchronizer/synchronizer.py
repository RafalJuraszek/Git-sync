import os
from time import sleep

from git import Repo
from git import exc
from datetime import datetime
import logging

def log(message, lvl = 0):
    print(message)

class SyncRepository:
    def __init__(self):
        self.localRepo = None
        self.origin = None
        self.remotes = []
    
    def initialize(self, local_path):
        self.localRepo = Repo(local_path)
        if not self.localRepo.bare:
            for r in self.localRepo.remotes:
                if r.name != 'origin':
                    self.remotes.append(r)
                else:
                    self.origin = r
        else:
            log(f'Repo not loaded correctly from {local_path}')
        return self

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
        """@remotes:param  - list of tuples (remote_name, url)"""
        for remote in remotes:
            self.add_remote(remote[1], remote[0])

    def generate_remote_name(self, remote: str):
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



def synchronization_loop(period, start: datetime):
    delay = datetime.now() - start

    sleep(delay.total_seconds() if delay.total_seconds() > 0 else 0)

    while True:
        start = datetime.now()
        local_repos = ['C:\\Users\\Adrian\\Studia\\IoTest']  # here we need db data
        for r in local_repos:
            repo = SyncRepository()
            try:
                repo.initialize(r)
            except exc.InvalidGitRepositoryError:
                url = 'https://'  # here we need db data
                repo.create(url, local_repos)
            remotes = [('bitbucket','https://bitbucket.org/IoTeamRak/test')]
            repo.add_remotes(remotes)
            repo.synchronize_all()
        time_to_wait = period - (datetime.now() - start).total_seconds()
        sleep(time_to_wait if time_to_wait > 0 else 0)


def synchronize2(sync_repo: SyncRepository):
    sync_repo.synchronize_all()


# repo = SyncRepository()
# # repo.create(r'https://github.com/Roshoy/test/', 'C:\\Users\\Adrian\\Studia\\IoTest')
# repo.initialize('C:\\Users\\Adrian\\Studia\\IoTest')
# repo.add_remote('https://bitbucket.org/IoTeamRak/test', 'bitbucket')
# # repo.initialize('C:\\Users\\Adrian\\Studia\\IoTest')
#
# synchronize2(repo)

synchronization_loop(30, datetime.now())