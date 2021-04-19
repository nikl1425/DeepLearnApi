import requests
import pandas as pd
from sqlalchemy import create_engine, insert
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import sessionmaker
from database.db_orm_obj import StockData, StockType, ForecastData

# API fetch key
API_KEY = "6a81f55d739d49c2a19610cd4a98e366"

""" OLD:
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(
    user="root",
    pw="Drageild07",
    db="Lstm",
    echo=True,
    pool_recycle=280
))

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(
    user="root",
    pw="Nvp92agn",
    host="35.242.209.129",
    db="NiklasRest",
    echo=True,
    pool_recycle=280
))
))
"""

# connection engine
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(
    user="root",
    pw="Nvp92agn",
    host="35.242.209.129",
    db="NiklasRest",
    echo=True,
    pool_recycle=280
))


# object relation mapping object
stock_data = StockData
stock_type = StockType

# session towards the database
Session = sessionmaker(bind=engine)
session = Session()


# get all types of stock we want to fetch
def get_all_stock_types():
    dict_stock_names = {}
    result = session.query(stock_type).all()
    for row in result:
        stock_id = row.id
        stock_name = row.stock_name
        dict_stock_names.update([(f"{stock_name}", stock_id)])
    print("got all types:  " + str(result))
    return dict_stock_names


# This function truncate stock_data and insert new values
def fetch_new_data():
    start_date = (datetime.now() - relativedelta(years=14)).strftime("%Y-%m-%d")
    end_date = datetime.today().strftime("%Y-%m-%d")
    close_time = "2021:24:00"
    try:
        truncate_stock_data()
        for key, value in get_all_stock_types().items():
            stock_name = key
            stock_id = value
            # fetch and pass to data var based on stock name, then we make it json
            data = requests.get(
            f"https://api.twelvedata.com/time_series?symbol={stock_name}&interval=1day&type=stock&format=JSON&start_date={start_date}%{close_time}&end_date={end_date}%{close_time}&apikey={API_KEY}")
            data = data.json()
            print("FETCHED SUCCES")
            for element in data["values"]:
                session.add_all([
                    StockData(datetime=element['datetime'],
                                open=element['open'],
                                high=element['high'],
                                low=element['low'],
                                close=element['close'],
                                volume=element['volume'],
                                stock_type_id=stock_id)
                    ])
                session.commit()
            print("inserted")
    except ValueError:
            print("something went wrong" + str(ValueError))


def insert_one():
    session.add_all([StockData(
        datetime="hej",
        open="test",
        close="test",
        high="test",
        low="test",
        volume="test",
        stock_type_id=1
    )])
    session.commit()

# this function truncates stock_data
def truncate_stock_data():
    with engine.connect() as con:
        con.execute('truncate stock_data')
    print("truncated stock_data")


def delete_from_forecast_on_typeid(id):
    with engine.connect() as con:
        con.execute('delete from forecast_data where stock_type_id=%s' %(id))


# This function returns a dataframe based of stock type name
def get_specific_stock_to_dataframe(name):
    id_of_stock = ""
    query = session.query(StockType).filter(StockType.name.like(name))
    for row in query:
        id_of_stock = row.id
    # now we query stock_data with the id and select all + pass to pandas dataframe
    data_of_stock = session.query(StockData).filter(StockData.stock_type_id==id_of_stock)
    df = pd.DataFrame([(d.datetime, d.open, d.high, d.low, d.close, d.volume) for d in data_of_stock],
                      columns=["datetime", "open", "high", "low", "close", "volume"])
    return df


# This function is for the iteration in the cron job
def get_all_types():
    query = session.query(StockType).all()
    types = []
    for row in query:
        # returns name for get specific_stock_to_dataframe
        types.append(row.name)
    print(types)
    return types


def get_stock_id_based_on_name(name):
    stock_type_id = None
    for type_id, in session.query(StockType.id).\
            filter_by(name=name):
                stock_type_id = type_id
    return stock_type_id


def insert_row_into_forecast(close_value, stock_type_id):
    row = ForecastData(close=close_value, stock_type_id=stock_type_id)
    session.add(row)
    session.commit()
    print("inserted: %s : %s - into forecast-table" %(close_value, stock_type_id))

def get_forecast_based_on_id(stock_id):
    data = session.query(ForecastData.close).filter_by(stock_type_id=stock_id)
    forecast_data = []
    for row in data:
        forecast_data.append(row.close)
    print(len(forecast_data))
    return forecast_data