import pandas as pd
from .models import DataSource, Stock
import datetime
import talib
import pathlib

def read_stock_from_file(path):
    df = pd.read_csv(path)
    data = df[['<DATE>','<TICKER>', '<OPEN>','<HIGH>','<LOW>','<CLOSE>','<VOL>']]
    return data


def add_to_database(df):
    instances = [DataSource(stock_symbol = Stock.objects.get(stock_symbol = stock[2]), day = datetime.datetime.strptime(str(stock[1]), '%Y%m%d'),
    volume = stock[7], stock_open = stock[3] , stock_high = stock[4] , stock_low = stock[5],  stock_close =stock[6]) for stock in df.itertuples(name=None)]
    DataSource.objects.bulk_create(instances)

def stocks_files_paths(dir):
    file_list = list(pathlib.Path(dir).glob('*.txt'))
    return file_list

def update_database():
    data_files_paths = stocks_files_paths(r"C:\\Users\\lukaa\Desktop\\d_pl_txt\\data\\daily\\pl\\wse stocks\\")
    for path in data_files_paths:
        stock_ticker = str(path).split('\\')[-1].split('.')[0].upper()
        search_value = DataSource.objects.filter(stock_symbol = stock_ticker)
        if search_value:
            if datetime.date.today() > search_value[len(search_value)-1].day:
                print('trzeba zaktualizowac')
        else:
            try:
                print(path)
                df = read_stock_from_file(path)
                add_to_database(df)
                print("dodane")
            except:
                print("Stock object doesnt exists")
                
def add_stock_informations():
    data_file = r"D:\\dev\\Scrapping\\dane.xlsx"
    data_source = pd.read_excel(data_file, index_col=0)  
    instances = [Stock(name = item[3], stock_symbol = item[2], isin = item[1], address = item[4], phone = item[5] , website = item[6]) 
                    for item in data_source.itertuples(name=None)]
    Stock.objects.bulk_create(instances)

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
    return df2

def stock_changes(stockname, period, option):
    df = get_stock_from_db(stockname.upper(), period)
    df['stock_changes'] = df['stock_close'].pct_change().round(4).dropna()*100
    if option == 1:
        return df['stock_changes'] 
    if option == 2:
        df2 = df[['day', 'stock_changes']]
        return df2
    if option == 3:
        df['rolling_mean'] = df['stock_changes'].rolling(5).mean().round(4).dropna()
        df3 = df[['day', 'rolling_mean']].dropna()
        return df3
