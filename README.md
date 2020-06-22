# Git-sync
> Application for synchronizing backup repositories (based on git - Github, Bitbucket, Gitlab etc.) with the main repository (on the github)

## Full Polish documentation (including "Developer documentation", "User documentation" etc.)
 link here
 
## Requirements
* [Python 3.8](https://www.python.org/downloads/)
* pip
* [pipenv](https://docs.python-guide.org/dev/virtualenvs/#installing-pipenv)
* [node](https://nodejs.org/en/download/)
* npm

## Running
* `git clone https://github.com/RafalJuraszek/Git-sync.git`
* `cd Git-sync`

### Server
* `pipenv install` - (installs the necessary dependencies based on the Pipfile file)
* `pipenv shell` - (creates an environment and automatically goes to it)
* `cd server`
* `python app.py`
### Management panel
#### Folders containing executable files:
* [Windows 10 (x64)](https://drive.google.com/file/d/1TAnPcomYw_2lBVPXJbAwzFK1YJpbFaIQ/view?usp=sharing)
* [macOS](https://drive.google.com/file/d/1btyLe4TVDgkOUJqjsyNE5VG3EAw2n3cm/view?usp=sharing)
* [Ubuntu (18)](https://drive.google.com/file/d/1Iy8Ghchl3x4hYE0HGabsGkm-UH2XjClO/view?fbclid=IwAR34zHpk-ciAWrx1l9mdEgrMKZcCvVHYMCfBsD9Mu0WnMfWvZONyHy2O0T0)

This folder can be generated for your operating system using the following commands (Node and npm required):
* `npm install -g @angular/cli`
* `npm install`
* `npm run pack`

After completing the above commands, a new directory should appear in the project containing files enabling direct launch of the client part.

## Contributors

* [Krzysztof Bieniasz](https://github.com/kbieniasz)
* [Rafał Juraszek](http://github.com/RafalJuraszek)
* [Adrian Maciej](https://github.com/Roshoy)
* [Benedykt Roszko](https://github.com/benroszko)
