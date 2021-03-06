import os
import shutil
from datetime import datetime
from threading import Event
from threading import Thread
from time import sleep

from database_maintenance.database_handler import ReposDatabaseHandler
from synchronizer.sync_repository import *

DataBaseHandler = ReposDatabaseHandler

logging.basicConfig(format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s',
                    level=logging.INFO, datefmt='%m/%d/%Y %H:%M:%S', filename='synchronizer_log.log')

def remove_remote(local_path, remote_url):
    """
    :param local_path: local path of repository
    :param remote_url: url to remote to delete
    """
    try:
        repo = Repo(local_path)
        if not repo.bare:
            repo.delete_remote(generate_remote_name(remote_url))
            log(f"Remote pointing to {remote_url} successfully removed")
    except KeyboardInterrupt:
        raise
    except Exception as e:
        log(f"Exception while removing branch: {e}", 2)


class Synchronizer:
    check_if_alive_period = 10

    def __init__(self):
        """threads - dictionary holding tuples of thread and event closing it, with keys as repository id"""
        self.threads = {}

    def synchronization_loop(self, repo_id, url, login, password, path, period, closing_event: Event):
        log(f'Synchronization loop started for {repo_id}')
        try:
            while True:
                start = datetime.now()
                repos_db = DataBaseHandler()
                repo = SyncRepository()
                try:
                    repo.initialize(path, login, password)
                except exc.InvalidGitRepositoryError:
                    repo.create(url, path, login, password)
                except ImportError:
                    raise

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
        except exc.GitCommandError as e:
            log(f'Error while creating local repository : {e}', 2)
        except exc.NoSuchPathError as e:
            log("No such path exception", 2)
        except KeyboardInterrupt:
            log(f'Closing {current_thread().name} with {repo_id}', 1)
        log('Synchronization loop stopped')

    def add_new_synchronization_thread(self, repo_id, url, login, password, path, period):
        try:
            if repo_id in self.threads.keys():
                log(f'{repo_id} is already being synchronized')
                return
            closing_event = Event()
            t = Thread(target=self.synchronization_loop, name=repo_id,
                       args=(repo_id, url, login, password, path, period, closing_event))
            t.start()
            self.threads[repo_id] = (t, closing_event)
        except Exception as e:
            log(f'Exception while creating thread for {repo_id} : {e}', 2)

    def synchronize_all_repos(self):
        # delay = datetime.now() - start
        # sleep(delay.total_seconds() if delay.total_seconds() > 0 else 0)
        # start = datetime.now()
        repos_db = DataBaseHandler()

        ids, urls, logins, passwords, paths, periods = repos_db.get_master_repos()

        for index in range(len(ids)):
            self.add_new_synchronization_thread(ids[index], urls[index], logins[index], passwords[index], paths[index],
                                                periods[index])

    def get_repository_local_path(self, repo_id):
        folder = ''
        try:
            repos_db = DataBaseHandler()
            ids, urls, logins, passwords, paths, periods = repos_db.get_master_repos()
            for i in range(len(ids)):
                if ids[i] == repo_id:
                    folder = paths[i]
                    break
        except Exception as e:
            log('Error while getting repository name from database', 2)
        return folder

    def remove_repository(self, repo_id):
        folder = self.get_repository_local_path(repo_id)
        if not folder:
            return
        try:
            self.end_synchronization_loop(repo_id)
            self.threads[repo_id][0].join()
        except KeyError:
            pass

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                log(f'Repository {repo_id} successfully removed')
            except Exception as e:
                log('Failed to delete %s. Reason: %s' % (file_path, e), 2)

    def end_synchronization_loop(self, repo_id):
        log(f'Closing synchronization loop for repository {repo_id} on thread {self.threads[repo_id][0].name}')
        self.threads[repo_id][1].set()

    def end_all_synchronization_loops(self):
        for id in self.threads.keys():
            self.end_synchronization_loop(id)
