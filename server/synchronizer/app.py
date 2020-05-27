
from flask import Flask, request, make_response
from synchronizer import synchronize
from flask import json
from json import JSONEncoder
from database_handler import ReposDatabaseHandler
from flask import jsonify
from notificator import notify
app = Flask(__name__)

@app.route("/api/addRepo", methods=['POST'])
def add_repo():
    data = request.get_json()
    master_repo_json = data.get('master', None)

    frequency = data.get('frequency', None)
    backups_json = data.get('backups', None)
    if master_repo_json == None or frequency == None or backups_json == None:
        print("DEBUG 1")
        return

    repos_db = ReposDatabaseHandler()
    # jednorazowo
    repos_db.create_master_repos_and_backup_repos_tables()

    repos_db.insert_data_master_repos(master_repo_json.get('id', None),
                                      master_repo_json.get('url', None),
                                      master_repo_json.get('login', None),
                                      master_repo_json.get('password', None),
                                      master_repo_json.get('path', None),
                                      frequency)

    for backup_repo in backups_json:
        repos_db.insert_backup_repos(master_repo_json.get('id', None),
                                     backup_repo.get('url', None),
                                     backup_repo.get('login', None),
                                     backup_repo.get('password', None) ,)

    repos_db.close()
    # to jest tylko jak sie bawilem w tworzenie odpowiedzi, moze sie przyda
    array = []
    array.append(Repo())
    response = app.response_class(
        response=json.dumps(array, cls = MyEncoder),
        status=200,
        mimetype='application/json'
    )
    # response = make_response("hello", 200)
    # response.mimetype = "text/plain"
    return response

@app.route("/api/modifyRepo", methods=['PUT'])
def modify_repo():
    data = request.get_json()
    master_repo_id = data.get('id', None)
    backups_json = data.get('backups', None)
    frequency = data.get('frequency', None)

    repos_db = ReposDatabaseHandler()
    repos_db.update_frequency_master_repos(id=master_repo_id, frequency=frequency)
    for backup_repo in backups_json:
        repos_db.update_or_create_backup_repo(master_repo_id,
                                              backup_repo.get('url', None),
                                              backup_repo.get('login', None),
                                              backup_repo.get('password', None))
    repos_db.close()
    response = app.response_class(
        response=[],
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/api/repos", methods=['GET'])
def get_repos():
    all_repos = []
    repos_db = ReposDatabaseHandler()

    ids, urls, logins, passwords, paths, frequencies = repos_db.get_master_repos()

    for id, url, login, password, path, frequency in zip(ids, urls, logins, passwords, paths, frequencies):
        repo = {'id': id, 'url' : url, 'login' : login,
                'password' : password, 'path' : path, 'frequency' : frequency}
        backup_repos = []
        for url, login, password in zip(urls, logins, passwords):
            backup = {'url' : url, 'login' : login, 'password' : password}
            backup_repos.append(backup)
        all_repos.add(repo)
    repos_db.close()

    return jsonify(all_repos)

@app.route("/api/repos/<id>", methods=['DELETE'])
def delete_repos(id):
    data = request.get_json()
    repos_db = ReposDatabaseHandler()
    # logika -> jak jest body to usuwamy tylko 1 konretny backup, jak bez body całe repo
    if data is None:
        repos_db.delete_master_repo(id)
    else:
        url = data.get('url', None)
        repos_db.delete_backup_repo(master_repo_id=id, url = url)

    repos_db.close()
    response = app.response_class(
        response=[],
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/api/notify", methods=['GET'])
def get_notify_data():
    data = request.get_json()
    notify(data.get('id', None))
    response = app.response_class(
        response=[],
        status=200,
        mimetype='application/json'
    )
    return response


class Repo:

    def __init__(self):
        self.id = 'ala'
        self.url = 'la'
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


if __name__ == "__main__":
    app.run(debug=True)
