import pandas as pd
from .models import DataSource
import datetime
import talib

def read_stock_from_file(path):
    df = pd.read_csv(path)
    data = df[['<DATE>','<TICKER>', '<OPEN>','<HIGH>','<LOW>','<CLOSE>','<VOL>']]
    return data

def add_to_database(df):
    instances = [DataSource(stock_symbol = stock[2], day = datetime.datetime.strptime(str(stock[1]), '%Y%m%d'),
    volume = stock[7], stock_open = stock[3] , stock_high = stock[4] , stock_low = stock[5],  stock_close =stock[6]) for stock in df.itertuples(name=None)]
    DataSource.objects.bulk_create(instances)

def get_stock_from_db(ticker, day_range):
    df = pd.DataFrame.from_records(DataSource.objects.filter(stock_symbol = ticker).values_list())
    df = df.rename(columns = {1:'stock_symbol',2:'day',3:'volume',4:'stock_open',5:'stock_high',6:'stock_low',7:'stock_close'})
    df = df.drop(columns = [0])
    return df.tail(day_range)

def bollinger_bands(stockname, period):
    df = get_stock_from_db(stockname.upper(), period)
    upper, middle, lower = talib.BBANDS(
        df['stock_close'], timeperiod=20, nbdevup=2,  nbdevdn=2)
    df['upper'] = upper
    df['middle'] = middle
    df['lower'] = lower
    df = df.set_index(df['day'])
    df.dropna(subset = ["upper","middle","lower"], inplace=True)
    return df

def rsi(stockname, period):
    df = get_stock_from_db(stockname.upper(), period)
    df = df.set_index(df['day'])
    rsi = talib.RSI(df['stock_close'])
    return rsi

def mean_volume(stockname, period):
    df = get_stock_from_db(stockname.upper(), period)
    df['rolling_volume'] = df['volume'].rolling(30).mean().round(4).dropna()
    df2 = df[['day','rolling_volume']]
    print(df2.dropna())
    return df2