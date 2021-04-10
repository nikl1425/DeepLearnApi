from model import Model
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import LSTM, Dense



class lstm(Model):
    def __init__(self, model_name):
        super().__init__(model_name)
        self.model_name = model_name

    def reformat_dataframe(self):
        # Load dataset from mySql
        self.load_data()
        self.dataframe = self.dataframe.set_index('datetime')
        # choosing only high, low, close column
        data = self.dataframe[['high', 'low', 'close']]
        # reverse data set
        data = data.iloc[::-1]
        #adding return and log_return col to
        cols = data.columns
        data[cols] = data[cols].apply(pd.to_numeric, errors='coerce')
        data['returns'] = data.close.pct_change()
        data['log_returns'] = np.log(1+data['returns'])
        data.dropna(inplace=True)
        return data

    def create_np_array(self):
        df = self.reformat_dataframe()
        # X-value for model
        x = df[['high', 'low', 'close', 'returns', 'log_returns']].values
        # Scale X sequence of data
        scaler = MinMaxScaler(feature_range=(0, 1)).fit(x)
        x_scaled = scaler.transform(x)
        y = [x[2] for x in x_scaled]
        return x_scaled, y

    def train_test_split_df(self):
        x, y = self.create_np_array()
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, shuffle=False)

        # Since we are working with timeseries data we create batches of sequences to predict next y
        train_gen = TimeseriesGenerator(data=x_train,
                                        targets=y_train,
                                        length=3,
                                        batch_size=1,
                                        shuffle=False,
                                        reverse=False,
                                        start_index=0,
                                        end_index=None)
        test_gen = TimeseriesGenerator(x_test,
                                       y_test,
                                       length=3,
                                       sampling_rate=1,
                                       batch_size=1,
                                       shuffle=False,
                                       reverse=False,
                                       start_index=0,
                                       end_index=None)
        return (train_gen, test_gen)

    def define_train__save_model(self):
        train_split, test_split = self.train_test_split_df()
        model = Sequential()
        model.add(LSTM(100, activation='relu', input_shape=(3, 5)))
        model.add(Dense(72, activation='relu'))
        model.add(Dense(1))
        model.compile(loss="mean_squared_error", optimizer="adam")
        model.fit_generator(
            train_split, steps_per_epoch=len(train_split), epochs=1
        )
        self.save_model(model, self.model_name)
        print(model.summary())



obj = lstm("apple")


