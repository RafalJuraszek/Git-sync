import os
from git import Repo
from git import RemoteProgress




if __name__ == "__main__":

    # Repo object used to programmatically interact with Git repositories
    #jesli plik ten jest w repo gita to bierze to repo (brak argumentu), mozna dac sciezke do folderu z gitem
    repo = Repo()
    # check that the repository loaded correctly
    if not repo.bare:

        origin = repo.remotes['origin']
        print(type(origin))
        origin.pull()
        #najpeirw trzeba stworzyc (ale to bysmy pewnie brali z arajki
        #repo1 = repo.create_remote('repo1', 'https://IoTeamRak@bitbucket.org/IoTeamRak/test2.git')
        repo1 = repo.remote(name='repo1')

        repo1.push()

    else:
        pass