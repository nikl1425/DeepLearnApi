from flask import Flask
from datetime import datetime
from flask_json import FlaskJSON, json_response
from flask_restful import Api
from flask_apscheduler import APScheduler
from machine_learning.model_object.lstm import lstm


# update 08-04

# Config Constants
one_day_in_seconds = 86400

# Model Objects
from task_manager import LstmForecast

# Basic Config:
app = Flask(__name__)
api = Api(app)
FlaskJSON(app)
scheduler = APScheduler()

# routing to machine_learning
api.add_resource(LstmForecast, '/api/lstm/<todo_id>')


@app.route('/hi')
def hello_world():
    now = datetime.utcnow()
    return json_response(time=now)


# Scheduled jobs
from database import mysql_connector


def schedulerTask():
    # Skal modificeres så den opdatere alle tables og alle modeller
    mysql_connector.fetch_new_data()
    # get all stock names
    all_stock_names = mysql_connector.get_all_types()
    # initialize
    # for all in stock_names create LSTM and run define_train_test
    for name in all_stock_names:
      model_object = lstm(str(name))
      model_object.define_train_save_model()


if __name__ == '__main__':
    scheduler.add_job(id='Shceduled tasks', func=schedulerTask, trigger='interval', days=1, next_run_time=datetime.now())
    scheduler.start()

    app.run(threaded=False, debug=False)
