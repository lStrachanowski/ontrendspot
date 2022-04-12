import pandas as pd
from .models import DataSource
import datetime

def read_stock_from_file(path):
    df = pd.read_csv(path)
    data = df[['<DATE>','<TICKER>', '<OPEN>','<HIGH>','<LOW>','<CLOSE>','<VOL>']]
    return data

def add_to_database(df):
    instances = [DataSource(stock_symbol = stock[2], day = datetime.datetime.strptime(str(stock[1]), '%Y%m%d'),
    volume = stock[7], stock_open = stock[3] , stock_high = stock[4] , stock_low = stock[5],  stock_close =stock[6]) for stock in df.itertuples(name=None)]
    DataSource.objects.bulk_create(instances)

def get_stock_from_db(ticker):
    stock = DataSource.objects.filter(stock_symbol = ticker)
    for e in stock:
        print(e.stock_symbol, e.volume)