import os
from git import Repo
from git import RemoteProgress


repos = ['https://gitlab.com/RafalJuraszek/io-test']

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