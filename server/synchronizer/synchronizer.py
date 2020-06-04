import os
import signal
from time import sleep
from threading import Thread
from threading import current_thread
from threading import Event

from git import Repo
from git import exc
from datetime import datetime
import logging

from server.db.database_handler import ReposDatabaseHandler


def log(message, lvl = 0):
    print('[' + current_thread().name + ']' + message)


class MockDb:
    def __init__(self):
        pass
#logins, passwords, paths, periods
    def get_master_repos(self):
        return (['test', 'test2'],
                ['https://github.com/Roshoy/test', 'https://github.com/Roshoy/test2'],
                ['Roshoy', 'Roshoy'],
                ['dummy', 'dummy'],
                [r'C:\Users\Adrian\Studia\IoTest', r'C:\Users\Adrian\Studia\IoTest2'],
                [30, 35])

    def get_backup_repos(self, master_repo_id):
        if master_repo_id == 'test':
            return (['https://bitbucket.org/IoTeamRak/test.git'],
                    ['IoTeamRak'],
                    ['Q1w2e3r4'])
        return (['https://bitbucket.org/IoTeamRak/test22.git'],
                ['IoTeamRak'],
                ['Q1w2e3r4'])


def generate_remote_name(remote):
    return remote.replace('/', '_').replace(':', '-').replace('?', '__').replace('.', '--')


def remove_remote(local_path, remote_url):
    try:
        repo = Repo(local_path)
        if not repo.bare:
            repo.delete_remote(generate_remote_name(remote_url))
    except KeyboardInterrupt:
        raise
    except Exception as e:
        log("Exception while removing branch", 3)
        log(e, 3)


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
        log(f"Local repository created at {local_path}")
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
        self.localRepo.git.fetch('--prune')
        self.localRepo.git.rebase()
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
            except KeyboardInterrupt:
                raise
            except Exception as e:
                log(e)

    def push_to_remotes(self):
        log(f'Pushing all')
        for remote, login, password in self.remotes:
            url = self.get_remote_url(remote, login, password)
            log(f'Pushing all to {url}')
            self.localRepo.git.push(url, '--all', '--force')
        log(f'All is pushed')

    def get_remote_url(self, remote, login, password):
        p = password.replace('@', '%40')
        url = next(remote.urls).split('//', 1)[1]
        url = f'https://{login}:{p}@{url}'
        if not url.endswith('.git'):
            url += '.git'
        return url

    def synchronize_all(self):
        # checkout to next branch
        log('Starting synchronization')
        self.pull_all()
        self.push_to_remotes()
        log('Synchronization ended')


class Synchronizer:
    check_if_alive_period = 10

    def __init__(self):
        """threads - dictionary holding tuples of thread and event closing it, with keys as repository id"""
        self.threads = {}

    def synchronization_loop(self, repo_id, url, login, password, path, period, closing_event: Event):
        log(f'Synchronization started for {repo_id}')
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

                while not closing_event.is_set() and time_to_wait > 0:
                    sleep(min(self.check_if_alive_period, period))
                    time_to_wait = period - (datetime.now() - start).total_seconds()

                if closing_event.is_set():
                    return

        except exc.NoSuchPathError as e:
            log("No such path exception")
        except KeyboardInterrupt:
            log(f'Closing {current_thread().name} with {repo_id}')

    def add_new_synchronization_thread(self, repo_id, url, login, password, path, period):
        try:
            if repo_id in self.threads.keys():
                log(f'{repo_id} is already being synchronized')
                return
            closing_event = Event()
            t = Thread(target=self.synchronization_loop,
                       args=(repo_id, url, login, password, path, period, closing_event))
            t.start()
            self.threads[repo_id] = (t, closing_event)
        except Exception as e:
            log(f'Exception while creating thread for {repo_id}')
            log(e)

    def synchronize_all_repos(self):
        # delay = datetime.now() - start
        # sleep(delay.total_seconds() if delay.total_seconds() > 0 else 0)
        # start = datetime.now()
        repos_db = MockDb()  # ReposDatabaseHandler()

        ids, urls, logins, passwords, paths, periods = repos_db.get_master_repos()

        for index in range(len(ids)):
            self.add_new_synchronization_thread(ids[index], urls[index], logins[index], passwords[index], paths[index],
                                                periods[index])

    def end_synchronization_loop(self, repo_id):
        log(f'Closing synchronization loop for repository {repo_id} on {self.threads[repo_id][0].name}')
        self.threads[repo_id][1].set()

    def end_all_synchronization_loops(self):
        for id in self.threads.keys():
            self.end_synchronization_loop(id)


# remove_remote('C:\\Users\\Adrian\\Studia\\IoTest', 'https://bitbucket.org/IoTeamRak/test.git')
s = Synchronizer()
s.synchronize_all_repos()

sleep(15)

s.end_synchronization_loop('test')

# repo = SyncRepository()
# # repo.create(r'https://github.com/Roshoy/test/', 'C:\\Users\\Adrian\\Studia\\IoTest')
# repo.initialize('C:\\Users\\Adrian\\Studia\\IoTest')
# repo.add_remote('https://bitbucket.org/IoTeamRak/test', 'bitbucket')
# # repo.initialize('C:\\Users\\Adrian\\Studia\\IoTest')
#
# synchronize2(repo)

