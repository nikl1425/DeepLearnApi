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
        self.forecast_sequence = None
        self.scaler = None

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
        self.scaler = scaler
        x_scaled = scaler.transform(x)
        y = [x[2] for x in x_scaled]
        return x_scaled, y

    def train_test_split_df(self):
        x, y = self.create_np_array()
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10, shuffle=False)

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
        self.train_generator = train_gen
        self.test_generator = test_gen
        return (train_gen, test_gen)


    # we need to store the sequence that we are going to start our forecast
    def generate_forecast_sequence(self, test_split_sequence, model):
        test_predict = model.predict_generator(test_split_sequence)
        test_predict = np.c_[test_predict,
                            np.zeros(test_predict.shape),
                            np.zeros(test_predict.shape),
                            np.zeros(test_predict.shape),
                            np.zeros(test_predict.shape)]
        test_predict = self.scaler.inverse_transform(test_predict)
        self.forecast_sequence = [element[0] for element in test_predict]
        print(len(test_predict))


    def define_train_save_model(self):
        train_split, test_split = self.train_test_split_df()
        model = Sequential()
        model.add(LSTM(100, activation='relu', input_shape=(3, 5)))
        model.add(Dense(72, activation='relu'))
        model.add(Dense(1))
        model.compile(loss="mean_squared_error", optimizer="adam")
        model.fit_generator(
            train_split, steps_per_epoch=len(train_split), epochs=1
        )
        # save the model to h5_file directory
        self.save_model(model, self.model_name)
        # set forecast sequence to class property
        self.generate_forecast_sequence(test_split, model)
        print(self.forecast_sequence)
        print(model.summary())

    def predict_with_model(self):
        returned_model = self.load_model()




obj = lstm("apple")
obj.define_train_save_model()


