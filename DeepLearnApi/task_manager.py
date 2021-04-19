from flask_restful import Resource
from database import mysql_connector
from flask_json import FlaskJSON, json_response



lstm_task = {
    'apple': {'task': 'return apple forecast'},
    'microsoft': {'task': 'return microsoft forecast'},
    'google': {'task': 'return google forecast'},
}


class LstmForecast(Resource):
    def get(self, todo_id):
        stock_type_id = mysql_connector.get_stock_id_based_on_name(todo_id)
        data = mysql_connector.get_forecast_based_on_id(stock_type_id)

        return json_response(status_=200, server_name='flask_deep', available=True, data=data, other_id_task=lstm_task)