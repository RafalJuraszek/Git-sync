from flask import Flask, request, make_response
from flask import json
from json import JSONEncoder
from server.db.database_handler import ReposDatabaseHandler
from flask import jsonify
from server.notificator.notificator import notify
from server.synchronizer.synchronizer import Synchronizer
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
    print("add repo request")
    print(request)
    print(request.get_json())
    data = request.get_json()
    print(data)

    frequency = data.get('frequency', None)
    backups_json = data.get('backups', None)
    if frequency == None or backups_json == None:
        print("DEBUG 1")
        return
    print("ok")
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

    print("db_communicate>>>>>>>>>> " + db_communicate)
    if not db_communicate == "ok":
        print("DEBUG>>>>>>>>>>")
        return send_400_db_error(db_communicate)


    for backup_repo in backups_json:
        repos_db.insert_data_backup_repos(data.get('id', None),
                                          backup_repo.get('url', None),
                                          backup_repo.get('login', None),
                                          backup_repo.get('password', None))

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

    for id, url, login, password, path, frequency in zip(ids, urls, logins, passwords, paths, frequencies):
        repo = {'id': id, 'url': url, 'login': login,
                'password': password, 'path': path, 'frequency': frequency}
        backup_repos = []
        urls_b, logins_b, passwords_b = repos_db.get_backup_repos(id)
        print(urls_b)
        print(logins_b)
        for url, login, password in zip(urls_b, logins_b, passwords_b):
            print("here")
            backup = {'url': url, 'login': login, 'password': password}
            backup_repos.append(backup)
        all_repos.append(repo)
    repos_db.close()
    print(all_repos)
    return jsonify(all_repos)


@app.route("/api/repos/<id>", methods=['DELETE'])
def delete_repos(id):
    data = request.get_json()
    repos_db = ReposDatabaseHandler()
    print(id)
    # logika -> jak jest body z urlem to usuwamy tylko 1 konretny backup, jak bez body całe repo
    data = request.get_json()
    print(data)
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
    return Response("{'message':'" + message+"'}", status=400, mimetype='application/json')

class Repo:

    def __init__(self):
        self.id = 'ala'
        self.url = 'la'


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


if __name__ == "__main__":
    print("start")
    synchronizer.synchronize_all_repos()
    app.run(debug=True)
