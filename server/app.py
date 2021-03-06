import signal
import sys
from time import sleep

import requests
from flask import Flask, request
from flask import json
from json import JSONEncoder
from database_maintenance.database_handler import ReposDatabaseHandler
from flask import jsonify
from notificator.email_client.notificator import notify
from synchronizer.synchronizer import Synchronizer
from database_maintenance.database_initializer import DatabaseInitializer
from flask import Response

app = Flask(__name__)

synchronizer = Synchronizer()


@app.route("/api/testget", methods=['GET'])
def get_test():
    print("get_test")
    response = app.response_class(
        response=json.dumps([], cls=MyEncoder),
        status=200,
        mimetype='application/json'
    )
    # response = make_response("hello", 200)
    # response.mimetype = "text/plain"
    return response


@app.route("/api/addRepo", methods=['POST'])
def add_repo():
    # print("add repo request")
    print(request)
    # print(request.get_json())
    data = request.get_json()
    print(data)

    frequency = data.get('frequency', None)
    backups_json = data.get('backups', None)
    if frequency == None or backups_json == None:
        return send_400_db_error("enter frequency and at least one backup repo")

    # print("ok")
    repos_db = ReposDatabaseHandler()
    # jednorazowo
    # repos_db.create_master_repos_and_backup_repos_tables()
    print(data.get('id', None))
    print(data.get('url', None))
    print(data.get('login', None))
    print(data.get('password', None))
    print(frequency)

    db_communicate = repos_db.insert_data_master_repos(data.get('id', None),
                                                       data.get('url', None),
                                                       data.get('login', None),
                                                       data.get('password', None),
                                                       data.get('path', None),
                                                       frequency)

    # print("db_communicate>>>>>>>>>> " + db_communicate)
    if not db_communicate == "ok":
        # print("DEBUG>>>>>>>>>>")
        return send_400_db_error(db_communicate)

    for backup_repo in backups_json:
        db_communicate = repos_db.insert_data_backup_repos(data.get('id', None),
                                                           backup_repo.get('url', None),
                                                           backup_repo.get('login', None),
                                                           backup_repo.get('password', None))

        if not db_communicate == "ok":
            print(db_communicate)
            # nie istotne dla uzytkownika

    repos_db.close()

    synchronizer.add_new_synchronization_thread(data.get('id', None),
                                                data.get('url', None),
                                                data.get('login', None),
                                                data.get('password', None),
                                                data.get('path', None),
                                                frequency)

    # to jest tylko jak sie bawilem w tworzenie odpowiedzi, moze sie przyda
    array = []
    # array.append(Repo())
    response = app.response_class(
        response=json.dumps(array, cls=MyEncoder),
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
    print("modify repo")
    repos_db = ReposDatabaseHandler()
    if frequency is not None:
        print("update frequency")
        repos_db.update_frequency_master_repos(id=master_repo_id, frequency=frequency)
    for backup_repo in backups_json:
        repos_db.update_or_create_backup_repo(master_repo_id,
                                              backup_repo.get('url', None),
                                              backup_repo.get('login', None),
                                              backup_repo.get('password', None))
    repos_db.close()
    array = []
    response = app.response_class(
        response=json.dumps(array, cls=MyEncoder),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/api/repos", methods=['GET'])
def get_repos():
    all_repos = []
    repos_db = ReposDatabaseHandler()

    tab = repos_db.get_master_repos()
    ids = tab[0]
    urls = tab[1]
    logins = tab[2]
    passwords = tab[3]
    paths = tab[4]
    frequencies = tab[5]
    print("get repos")
    for id, url, login, password, path, frequency in zip(ids, urls, logins, passwords, paths, frequencies):
        repo = {'id': id, 'url': url, 'login': login,
                'password': password, 'path': path, 'frequency': frequency}
        backup_repos = []
        urls_b, logins_b, passwords_b = repos_db.get_backup_repos(id)
        print(logins_b)
        for url, login, password in zip(urls_b, logins_b, passwords_b):
            backup = {'url': url, 'login': login, 'password': password}
            backup_repos.append(backup)
        repo['backups'] = backup_repos
        all_repos.append(repo)
    repos_db.close()
    print(all_repos)
    return jsonify(all_repos)


@app.route("/api/repos/<id>", methods=['DELETE'])
def delete_repos(id):
    print("DELETE handler")
    repos_db = ReposDatabaseHandler()
    print(id)
    # logika -> jak jest body z urlem to usuwamy tylko 1 konretny backup, jak bez body całe repo
    data = request.get_json()
    if data is None:
        print("delete master")
        repos_db.delete_master_repo(id)
    else:
        url = data.get('url', None)
        print("delete " + url)
        repos_db.delete_backup_repo(master_repo_id=id, url=url)

    repos_db.close()
    response = app.response_class(
        response=[],
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/api/notify", methods=['POST'])
def get_notify_data():
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> NOTIFY")
    data = request.get_json()
    print("notify DEBUG")
    print(data)
    id = data.get('id', None)
    # na ten moment nic nie przychodzi z frontu
    if id is None:
        print("sztuczne przypisanie")
        id = 'dobry_url'
    # print("DEBUG ID -> " + id)
    notify(id)
    response = app.response_class(
        response=[],
        status=200,
        mimetype='application/json'
    )
    return response


def send_400_db_error(message):
    return Response("{\"message\":\"" + message + "\"}", status=400, mimetype='application/json')


class Repo:

    def __init__(self):
        self.id = 'ala'
        self.url = 'la'


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    print("Shutting down starts")
    synchronizer.end_all_synchronization_loops()
    shutdown_server()
    print("Shutting down starts")
    return 'Server shutting down...'

def thread_webAPP():
    print("start")
    db_init = DatabaseInitializer()
    db_init.create_tables_if_not_exist()
    synchronizer.synchronize_all_repos()
    app.run(debug=True)


if __name__ == "__main__":
    print("start")

    def handler(signal, frame):
        try:
            print('CTRL-C pressed!')
            requests.post('http://127.0.0.1:5000/shutdown')
            sleep(1)
            sys.exit(0)
        except:
            sys.exit(0)

    signal.signal(signal.SIGINT, handler)

    db_init = DatabaseInitializer()
    db_init.create_tables_if_not_exist()
    synchronizer.synchronize_all_repos()
    app.run(debug=True)
