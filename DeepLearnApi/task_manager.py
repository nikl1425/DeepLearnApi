from flask_restful import Resource


LSTM = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


class LstmForecast(Resource):
    def get(self, todo_id):

        #put in mapping logic for task list

        return LSTM[todo_id]