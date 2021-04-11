from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

Base = declarative_base()


class StockData(Base):
    __tablename__ = 'stock_data'

    id = Column(Integer, primary_key=True)
    datetime = Column(String)
    open = Column(String)
    high = Column(String)
    low = Column(String)
    close = Column(String)
    volume = Column(String)
    stock_id = Column(Integer)

    def __repr__(self):
        return "<Stockdata(id='%s', datetime='%s' open='%s', high='%s', low='%s', close='%s', volume='%s', stock_id='%s')>" % (
            self.id, self.datetime, self.open, self.high, self.low, self.close, self.volume, self.stock_id
        )


class StockType(Base):
    __tablename__ = 'stock_type'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    stock_name = Column(String)

    def __repr__(self):
        return "<StockType(id='%s', name='%s', stock_name='%s')>" % (
            self.id, self.name, self.stock_name
        )


class ForecastData(Base):
    __tablename__ = 'forecast_data'

    id = Column(Integer, primary_key=True)
    close = Column(Integer)
    stock_type_id = Column(Integer)

    def __repr__(self):
        return "<ForecastData(id='%s', close='%s', stock_type_id='%s')>" % (
            self.id, self.close, self.stock_type_id
        )