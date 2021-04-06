from flask import Flask, request, jsonify
from datetime import datetime
from flask_json import FlaskJSON, json_response
import pandas as pd
from flask_restful import Api
import time


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




if __name__ == '__main__':
   app.run()