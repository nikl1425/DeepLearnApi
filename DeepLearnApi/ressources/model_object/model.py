import pandas as pd
from sqlalchemy import create_engine

"""
The main purpose of this class is constructing a parent class for the different model objects.
task 1: Load models
task 2: Save models
"""

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(
    user="root",
    pw="Drageild07",
    db="Lstm"
))

class Model():
    def __init__(self, name, database_name):
        self.name = name
        self.database_name = database_name
        self.data = pd.DataFrame()

    def load_data(self, database_name):
        data_raw = pd.read_sql(database_name, con=engine)
        data_raw['close'] = data_raw['close'].astype(float)
        return data_raw

    def load_model(self, name):
        pass


    def save_model(self, model_object):
        pass