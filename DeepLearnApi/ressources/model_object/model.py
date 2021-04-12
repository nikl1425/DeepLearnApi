import pandas as pd
from database import mysql_connector
import pandas as pd
import keras

"""
The main purpose of this class is constructing a parent class for the different model objects.
task 1: Load models
task 2: Save models
"""


class Model():
    def __init__(self, name):
        self.name = name
        self.dataframe = pd.DataFrame()
        self.model = ""

    def load_data(self):
        df = mysql_connector.get_specific_stock_to_dataframe(self.name)
        self.dataframe = pd.DataFrame(df)

    def save_lstm_model(self, model_object, object_name):
        model_object.save(f'../h5_file/lstm_{object_name}.h5')
        print(f"model: {object_name} saved!")

    def load_lstm_model(self):
        reconstructed_model = keras.models.load_model(f'../h5_file/lstm_{self.name}.h5')
        return reconstructed_model


