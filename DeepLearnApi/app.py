from flask import Flask, request, jsonify
from datetime import datetime
from flask_json import FlaskJSON, json_response
import pandas as pd
from flask_restful import Api

# Model Objects
from task_manager import LstmForecast

# Basic Config:
app = Flask(__name__)
api = Api(app)
FlaskJSON(app)

# routing to ressources
api.add_resource(LstmForecast, '/api/lstm/<todo_id>')



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
        print(key_list)
        df = pd.DataFrame(data)
        print(len(df))
        #df.to_csv(r'/Users/niklashjort/Desktop/Projects/DeepLearnApi/DeepLearnApi/training/data/apple_data.csv', index=False, header=True)
        return jsonify(data)
    else:
            error = 'Invalid username/password'
            return print(error)
    # the code below is executed if the request method
    # was GET or the credentials were invalid


if __name__ == '__main__':
   app.run()