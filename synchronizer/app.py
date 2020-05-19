from flask import Flask, request, make_response
from synchronizer import synchronize
from flask import jsonify
app = Flask(__name__)

@app.route("/synchronizer")
def hello():
    synchronize()
    #to jest tylko jak sie bawilem w tworzenie odpowiedzi, moze sie przyda
    response = make_response("hello", 200)
    response.mimetype = "text/plain"
    return jsonify('{"status":"ok"}')



if __name__ == "__main__":
    app.run(debug=True)