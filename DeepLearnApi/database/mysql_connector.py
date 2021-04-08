import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from dateutil.relativedelta import relativedelta

# update 08-04

API_KEY = "6a81f55d739d49c2a19610cd4a98e366"

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(
    user="root",
    pw="Drageild07",
    db="Lstm"
))
last = datetime.now() - relativedelta(years=5)
last = last.strftime("%Y-%m-%d")
print(last)

def fetch_from_api(name):
    start_date = (datetime.now() - relativedelta(years=14)).strftime("%Y-%m-%d")
    end_date = datetime.today().strftime("%Y-%m-%d")
    close_time = "2021:24:00"
    data = requests.get(f"https://api.twelvedata.com/time_series?symbol={name}&interval=1day&type=stock&format=JSON&start_date={start_date}%{close_time}&end_date={end_date}%{close_time}&apikey={API_KEY}")
    print("SUCCESS")
    return data.json()

def update_apple():
    request = fetch_from_api("AAPL")
    request = request["values"]
    request = pd.DataFrame(request)
    request = request.iloc[::-1]
    try:
        request.to_sql("apple", con=engine, if_exists='replace', chunksize=1000, index=False)
        print("appended")
    except:
        print("could not append or maybe connect")
update_apple()