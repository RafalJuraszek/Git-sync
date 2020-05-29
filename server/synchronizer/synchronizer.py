import os
from time import sleep
from threading import Thread

from git import Repo
from git import exc
from datetime import datetime
import logging

from server.db.database_handler import ReposDatabaseHandler


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
            new_remote = self.localRepo\
                .create_remote(remote_name if remote_name != '' else self.generate_remote_name(remote_url), remote_url)
            self.remotes.append(new_remote)
        except exc.GitCommandError as e:
            log(e)

    def add_remotes(self, remotes):
        """@remotes:param  - list of tuples (remote_name, url)"""
        for remote in remotes:
            self.add_remote(remote[1], remote[0])

    def generate_remote_name(self, remote: str):
        return remote.replace('r','l')

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


class Synchronizer:
    def __init__(self):
        self.threads = []

    def synchronization_loop(self, repo_id, url, login, password, path, period):
        while True:
            start = datetime.now()
            repos_db = ReposDatabaseHandler()
            repo = SyncRepository()
            try:
                repo.initialize(path)
            except exc.InvalidGitRepositoryError:
                repo.create(url, path)
            remote_repos = repos_db.get_backup_repos(repo_id)
            remotes = [('', url) for url in remote_repos[0]]  # [('bitbucket','https://bitbucket.org/IoTeamRak/test')]
            repo.add_remotes(remotes)
            repo.synchronize_all()

            time_to_wait = period - (datetime.now() - start).total_seconds()
            sleep(time_to_wait if time_to_wait > 0 else 0)

    def add_new_synchronization_thread(self, repo_id, url, login, password, path, period):
        t = Thread(target=self.synchronization_loop,
                   args=(repo_id, url, login, password, path, period))
        t.start()
        self.threads.append(t)

    def synchronize_all_repos(self):
        # delay = datetime.now() - start
        #
        # sleep(delay.total_seconds() if delay.total_seconds() > 0 else 0)

        # start = datetime.now()
        repos_db = ReposDatabaseHandler()

        repos = repos_db.get_master_repos()

        ids = repos[0]
        urls = repos[1]
        logins = repos[2]
        passwords = repos[3]
        paths = repos[4]
        periods = repos[5]    # local_repos = ['C:\\Users\\Adrian\\Studia\\IoTest']  # here we need db data

        for index in range(len(ids)):
            self.add_new_synchronization_thread(ids[index], urls[index], logins[index], passwords[index], paths[index],
                                                periods[index])

    def end_synchronization_loops(self):
        pass

# repo = SyncRepository()
# # repo.create(r'https://github.com/Roshoy/test/', 'C:\\Users\\Adrian\\Studia\\IoTest')
# repo.initialize('C:\\Users\\Adrian\\Studia\\IoTest')
# repo.add_remote('https://bitbucket.org/IoTeamRak/test', 'bitbucket')
# # repo.initialize('C:\\Users\\Adrian\\Studia\\IoTest')
#
# synchronize2(repo)

