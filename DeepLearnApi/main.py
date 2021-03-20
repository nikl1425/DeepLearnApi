from flask import Flask, request,jsonify
from datetime import datetime
from flask_json import FlaskJSON, JsonError, json_response, as_json
import json
from types import SimpleNamespace


app = Flask(__name__)
FlaskJSON(app)


def do_the_login():
    return print("what")



@app.route('/')
def hello_world():
    now = datetime.utcnow()
    return json_response(time=now)


@app.route('/api/modelOne', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        print("hi")
        data = request.get_json()
        print(data['lastname'])
        return jsonify(data)
    else:
            error = 'Invalid username/password'
            return print(error)
    # the code below is executed if the request method
    # was GET or the credentials were invalid



if __name__ == '__main__':
   app.run()