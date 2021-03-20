from flask import Flask, request,jsonify
from datetime import datetime
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_cors import CORS
import json
import json
from types import SimpleNamespace
import pandas as pd


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
        key_list = [k for k, v in data[0].items()]
        df = pd.DataFrame(data)

        df.to_csv(r'C:\Users\45535\Desktop\Informatik 3 semester\project\DeepLearnApi\training\export_dataframe.csv', index=False, header=True)
       # [kv for d in ld for kv in d.items()]



        return jsonify(data)
    else:
            error = 'Invalid username/password'
            return print(error)
    # the code below is executed if the request method
    # was GET or the credentials were invalid



if __name__ == '__main__':
   app.run()