import requests
import pandas as pd
from sqlalchemy import create_engine



engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(
    user="root",
    pw="Drageild07",
    db="Lstm"
))

def update_apple():
    r = requests.get("https://api.twelvedata.com/time_series?symbol=AAPL&interval=1day&type=stock&format=JSON&start_date=2014-01-01%2021:24:00&end_date=2021-03-19%2021:24:00&apikey=6a81f55d739d49c2a19610cd4a98e366")
    r = r.json()
    r = r["values"]
    r = pd.DataFrame(r)
    r = r.iloc[::-1]
    try:
        r.to_sql("apple", con=engine, if_exists='append', chunksize=1000, index=False)
        print("appended")
    except:
        print("could not append or maybe connect")

update_apple()