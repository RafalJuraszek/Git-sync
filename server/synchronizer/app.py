from flask import Flask, request, make_response
from synchronizer import synchronize
from flask import json
from json import JSONEncoder
app = Flask(__name__)

@app.route("/api/repos")
def hello():
    #synchronize()
    #to jest tylko jak sie bawilem w tworzenie odpowiedzi, moze sie przyda
    array = []
    array.append(Repo())
    response = app.response_class(
        response=json.dumps(array, cls = MyEncoder),
        status=200,
        mimetype='application/json'
    )
    #response = make_response("hello", 200)
    #response.mimetype = "text/plain"   
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