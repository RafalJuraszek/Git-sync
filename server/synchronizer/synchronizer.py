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


class MockDb:
    def __init__(self):
        pass
#logins, passwords, paths, periods
    def get_master_repos(self):
        return (['test'],
                ['https://github.com/Roshoy/test'],
                ['Roshoy'],
                ['not using you chicky wanker'],
                [r'C:\Users\Adrian\Studia\IoTest'],
                [30])

    def get_backup_repos(self, master_repo_id):
        return (['https://bitbucket.org/IoTeamRak/test.git'],
                ['IoTeamRak'],
                ['Q1w2e3r4'])


def generate_remote_name(remote):
    return remote.replace('/','_').replace(':', '-').replace('?', '_')


class SyncRepository:
    def __init__(self):
        self.localRepo = None
        self.origin = None
        self.remotes = []
    
    def initialize(self, local_path, login, password):
        self.localRepo = Repo(local_path)
        if not self.localRepo.bare:
            for r in self.localRepo.remotes:
                if r.name != 'origin':
                    self.remotes.append([r, login, password])  # setting same password as for master
                else:
                    self.origin = (r, login, password)
        else:
            log(f'Repo not loaded correctly from {local_path}')
        return self

    def create(self, origin, local_path, login, password):
        Repo.clone_from(origin, local_path)
        self.initialize(local_path, login, password)
        self.localRepo.git.config('remote.origin.prune', 'true')
        return self
    
    def add_remote(self, remote_url, login, password):
        try:
            for remote in self.remotes:
                url = next(remote[0].urls)
                log(f'Checking if we have same remote already on {url}')
                if url == remote_url:
                    remote[1] = login
                    remote[2] = password
                    return
            new_remote = self.localRepo\
                .create_remote(generate_remote_name(remote_url), remote_url)
            self.remotes.append([new_remote, login, password])
        except exc.GitCommandError as e:
            log(e)

    def add_remotes(self, remotes):
        """@remotes:param  - list of tuples (url, login, password)"""
        for remote in remotes:
            self.add_remote(remote[0], remote[1], remote[2])

    def pull(self):
        self.localRepo.git.pull('--rebase')
        self.localRepo.git.submodule('update', '--recursive')

    def pull_all(self):
        for ref in self.origin[0].refs:
            try:
                branch_name = ref.name.split('/')[1]
                if branch_name == 'HEAD':
                    continue
                log(f'Pulling {branch_name} from origin')
                self.localRepo.git.checkout(branch_name, '--force')
                self.pull()
                log(f'Pulled {branch_name} from origin')
            except Exception as e:
                log(e)

    def push_to_remotes(self):
        log(f'Pushing all')
        for remote, login, password in self.remotes:
            p = password.replace('@', '%40')
            url = next(remote.urls).split('//', 1)[1]
            url = f'https://{login}:{p}@{url}'
            log(f'Pushing all to {url}')
            self.localRepo.git.push(url, '--all', '--force')

    def synchronize_all(self):
        # checkout to next branch
        self.pull_all()
        self.push_to_remotes()


class Synchronizer:
    def __init__(self):
        self.threads = []

    def synchronization_loop(self, repo_id, url, login, password, path, period):
        try:
            while True:
                start = datetime.now()
                repos_db = MockDb()  # ReposDatabaseHandler()
                repo = SyncRepository()
                try:
                    repo.initialize(path, login, password)
                except exc.InvalidGitRepositoryError:
                    repo.create(url, path, login, password)
                remote_repos = repos_db.get_backup_repos(repo_id)
                remote_credentials = []
                for i in range(len(remote_repos[0])):
                    remote_credentials.append((remote_repos[0][i], remote_repos[1][i], remote_repos[2][i]))
                repo.add_remotes(remote_credentials)

                repo.synchronize_all()

                time_to_wait = period - (datetime.now() - start).total_seconds()
                sleep(time_to_wait if time_to_wait > 0 else 0)
        except exc.NoSuchPathError as e:
            log("No such path exception")

    def add_new_synchronization_thread(self, repo_id, url, login, password, path, period):
        t = Thread(target=self.synchronization_loop,
                   args=(repo_id, url, login, password, path, period))
        t.start()
        self.threads.append(t)

    def synchronize_all_repos(self):
        # delay = datetime.now() - start
        # sleep(delay.total_seconds() if delay.total_seconds() > 0 else 0)
        # start = datetime.now()
        repos_db = MockDb()  # ReposDatabaseHandler()

        ids, urls, logins, passwords, paths, periods = repos_db.get_master_repos()
        # local_repos = ['C:\\Users\\Adrian\\Studia\\IoTest']  # here we need db data

        for index in range(len(ids)):
            self.add_new_synchronization_thread(ids[index], urls[index], logins[index], passwords[index], paths[index],
                                                periods[index])

    def end_synchronization_loops(self):
        pass


s = Synchronizer()
s.synchronize_all_repos()

# repo = SyncRepository()
# # repo.create(r'https://github.com/Roshoy/test/', 'C:\\Users\\Adrian\\Studia\\IoTest')
# repo.initialize('C:\\Users\\Adrian\\Studia\\IoTest')
# repo.add_remote('https://bitbucket.org/IoTeamRak/test', 'bitbucket')
# # repo.initialize('C:\\Users\\Adrian\\Studia\\IoTest')
#
# synchronize2(repo)

