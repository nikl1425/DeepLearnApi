from flask import Flask
from datetime import datetime
from flask_json import FlaskJSON, json_response
from flask_restful import Api
from flask_apscheduler import APScheduler

# Config Constants
one_day_in_seconds = 86400

# Model Objects
from task_manager import LstmForecast

# Basic Config:
app = Flask(__name__)
api = Api(app)
FlaskJSON(app)
scheduler = APScheduler()

# routing to ressources
api.add_resource(LstmForecast, '/api/lstm/<todo_id>')


@app.route('/')
def hello_world():
    now = datetime.utcnow()
    return json_response(time=now)


# Scheduled jobs
from database import mysql_connector


def schedulerTask():
    # Skal modificeres så den opdatere alle tables og alle modeller
    mysql_connector.update_apple()


if __name__ == '__main__':
    scheduler.add_job(id='Shceduled tasks', func=schedulerTask, trigger='interval', seconds=one_day_in_seconds)
    scheduler.start()
    app.run()
