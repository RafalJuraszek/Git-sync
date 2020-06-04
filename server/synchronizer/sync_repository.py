from threading import current_thread

from git import Repo
from git import exc


def log(message, lvl=0):
    print('[' + current_thread().name + ']' + message)


def generate_remote_name(remote):
    return remote.replace('/', '_').replace(':', '-').replace('?', '__').replace('.', '--')


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
            new_remote = self.localRepo \
                .create_remote(generate_remote_name(remote_url), remote_url)
            self.remotes.append([new_remote, login, password])
        except exc.GitCommandError as e:
            log(e)

    def add_remotes(self, remotes):
        """:param remotes: iterable of tuples (url, login, password)"""
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

