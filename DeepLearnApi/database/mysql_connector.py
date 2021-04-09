import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import sessionmaker
from database.db_orm_obj import StockData

# API fetch key
API_KEY = "6a81f55d739d49c2a19610cd4a98e366"

# connection engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(
    user="root",
    pw="Nvp92agn",
    db="stock",
    echo=True # Logging
))

# object relation mapping object
stock_data = StockData


def fetch_from_api(name):
    start_date = (datetime.now() - relativedelta(years=14)).strftime("%Y-%m-%d")
    end_date = datetime.today().strftime("%Y-%m-%d")
    close_time = "2021:24:00"
    print("start:  "+ str(start_date) + "  end :  " + str(end_date))
    data = requests.get(f"https://api.twelvedata.com/time_series?symbol={name}&interval=1day&type=stock&format=JSON&start_date={start_date}%{close_time}&end_date={end_date}%{close_time}&apikey={API_KEY}")
    print("SUCCESS")
    return data.json()


def get_all_stock_types():
    pass

def update_apple():
    stock_name = "AAPL"
    request = fetch_from_api("AAPL")
    request = request["values"]
    request = pd.DataFrame(request)
    request = request.iloc[::-1]
    try:
        request.to_sql("apple", con=engine, if_exists='replace', chunksize=1000, index=False)
        print("appended")
    except ValueError:
        print("could not append or maybe connect" + str(ValueError))
update_apple()


Session = sessionmaker(bind = engine)
session = Session()
result = session.query(stock_data).all()

for row in result:
    print("name: ", row.open)