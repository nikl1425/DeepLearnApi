from .model import Model
import numpy as np
import pandas as pd


class lstm(Model):
    def __init__(self, model_name, database_name):
        super().__init__(model_name, database_name)
        self.database_name = database_name

    def reformat_data(self):
        # Load dataset from mySql
        dataFrame = self.load_data(self.database_name)

        # Select and adding columns for log and raw percentage change between each datapoint
        dataFrame = dataFrame[['high', 'low', 'close']]
        dataFrame['returns'] = dataFrame.close.pct_change()

        print(dataFrame.close)

    def train_model(self):
        pass


obj = lstm("apple", 'apple')
obj.reformat_data()