from threading import current_thread

from git import Repo
from git import exc


def log(message, lvl=0):
    print('[' + current_thread().name + ']' + str(message))


def generate_remote_name(remote):
    return remote.replace('/', '_').replace(':', '-').replace('?', '__').replace('.', '--')


class SyncRepository:
    def __init__(self):
        self.localRepo = None
        self.origin = None
        self.remotes = []

    def initialize(self, local_path, login, password):
        log(f'Loading repository {local_path}')
        self.localRepo = Repo(local_path)
        if not self.localRepo.bare:
            for r in self.localRepo.remotes:
                if r.name != 'origin':
                    self.remotes.append([r, login, password])  # setting same password as for master
                else:
                    self.origin = (r, login, password)
            log(f'Repo loaded from {local_path}')
        else:
            log(f'Repo not loaded correctly from {local_path}')
        return self

    def create(self, origin, local_path, login, password):
        log(f'Creating repository at {local_path}')
        Repo.clone_from(origin, local_path)
        self.initialize(local_path, login, password)
        self.localRepo.git.config('remote.origin.prune', 'true')
        log(f"Local repository created at {local_path}")
        return self

    def add_remote(self, remote_url, login, password):
        try:
            rem_name = generate_remote_name(remote_url)
            for remote in self.remotes:
                log(f'Checking if we have same remote already on {remote[0].name}')
                if rem_name == remote[0].name:
                    remote[1] = login
                    remote[2] = password
                    return
            new_remote = self.localRepo \
                .create_remote(rem_name, remote_url)
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

    def get_all_branches(self):
        return [line.strip() for line in self.localRepo.git.branch().replace('*', ' ').splitlines()]

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

    def get_remote_branches(self, remote):
        lines = self.localRepo.git.ls_remote('--heads', remote.name).splitlines()
        return [branch.split()[1].split('heads/')[1] for branch in lines]

    def push_to_remotes(self):
        log(f'Pushing all')
        for remote, login, password in self.remotes:
            print(self.get_remote_branches(remote))
            current_branches = self.get_all_branches()
            url = self.get_remote_url(remote, login, password)
            log(f'Pushing all to {remote.name}')
            for ref in remote.refs:
                branch_name = ref.name.split('/')[1]
                if branch_name == 'HEAD':
                    continue
                if branch_name not in current_branches:
                    self.localRepo.git.push(url, '--delete', branch_name)
                    log(f'Deleted remote branch {branch_name} from remote {remote.name}')

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

