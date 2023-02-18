import pandas as pd
import numpy as np
from .models import DataSource, Stock, DayList
import datetime
import talib
import pathlib
from datetime import timedelta, datetime, date


def read_stock_from_file(path):
    df = pd.read_csv(path)
    data = df[['<DATE>', '<TICKER>', '<OPEN>',
               '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']]
    return data

# Is adding stocks data to database
def add_to_database(df):
    instances = [DataSource(stock_symbol=Stock.objects.get(stock_symbol=stock[2]), day=datetime.strptime(str(stock[1]), '%Y%m%d'),
                            volume=stock[7], stock_open=stock[3], stock_high=stock[4], stock_low=stock[5],  stock_close=stock[6]) for stock in df.itertuples(name=None)]
    DataSource.objects.bulk_create(instances)

# Is adding single stock data to database 
def add_stock_entry_to_db(stock_data):
    new_entry = DataSource.objects.create(stock_symbol=Stock.objects.get(stock_symbol=stock_data['<TICKER>']), day=datetime.strptime(str(stock_data['<DATE>']), '%Y%m%d'),
                                          volume=stock_data['<VOL>'], stock_open=stock_data['<OPEN>'], stock_high=stock_data['<HIGH>'], stock_low=stock_data['<LOW>'],  stock_close=stock_data['<CLOSE>'])
    new_entry.save()            

# Is adding daylist values to database 
def add_daylist_to_db(df,option):
    if option == 'V':
        instances = [DayList.objects.create(option = 'V', day = stock['Date'], stock_symbol = Stock.objects.get(stock_symbol=stock['Ticker']) , volume = stock['Change']  ) for i, stock in df.iterrows()]
        DayList.objects.bulk_create(instances)
    if option == 'M':
        instances = [DayList.objects.create(option = 'M', day = stock['Date'], stock_symbol = Stock.objects.get(stock_symbol=stock['Ticker']) , volume = stock['Change']  ) for i, stock in df.iterrows()]
        DayList.objects.bulk_create(instances)


def stocks_files_paths(dir):
    file_list = list(pathlib.Path(dir).glob('*.txt'))
    return file_list

def read_mean_volumen():
    df = pd.DataFrame.from_records(DayList.objects.filter(option = 'V').values_list())
    df = df.drop(columns=[0,4,5])
    df = df.rename(columns={1: 'option', 2: 'day', 3: 'stock_symbol',6: 'percent_change'})
    df = df.groupby(by=['day'])
    return df

# Is adding missing stocks details to database, which were not importet correctly by scrapping
def add_missing_stock_data():
    PATH = r'D:\\dev\\Scrapping\\danespolek.txt'
    df = pd.read_csv(PATH)
    database =  [v.stock_symbol  for v in Stock.objects.all()]
    instances = []
    for i, item in df.iterrows():
        if item['stock_symbol'] not in database:
            instances.append(Stock(name=item['name'], stock_symbol=item['stock_symbol'], isin=item['isin'], address=item['address'], phone=item['phone'], website=item['website']))
    Stock.objects.bulk_create(instances)
    print("dodane")

# Update database base on new daily stock data
def update_database(option):
    PATH = ''
    if option == 'wse':
        PATH_WSE = r"C:\\Users\\lukaa\Desktop\\d_pl_txt\\data\\daily\\pl\\wse stocks\\"
        PATH = PATH_WSE
    if  option == 'nc':
        PATH_NC =  r"C:\\Users\\lukaa\Desktop\\d_pl_txt\\data\\daily\\pl\\nc stocks\\"
        PATH = PATH_NC
    data_files_paths = stocks_files_paths(PATH)
    for path in data_files_paths:
        stock_ticker = str(path).split('\\')[-1].split('.')[0].upper()
        search_value = DataSource.objects.filter(stock_symbol=stock_ticker)
        if search_value:
            current_stock_data = read_stock_from_file(
                PATH + stock_ticker + ".txt")
            stock_time = datetime.strptime(
                str(current_stock_data['<DATE>'].iloc[-1]), '%Y%m%d')
            if stock_time.date() > search_value[len(search_value)-1].day:
                for index, new_stock_data in current_stock_data.iterrows():
                    if datetime.strptime(str(new_stock_data['<DATE>']), '%Y%m%d').date() > search_value[len(search_value)-1].day:
                        add_stock_entry_to_db(new_stock_data)
                        print(new_stock_data['<TICKER>'], new_stock_data['<DATE>'],"Stock data added")
            else:
                print("Nothing to add.")
        else:
            try:
                print(path)
                df = read_stock_from_file(path)
                add_to_database(df)
                print("Added")
            except:
                print("Stock object doesnt exists")


def add_stock_informations():
    data_file = r"D:\\dev\\Scrapping\\dane.xlsx"
    data_source = pd.read_excel(data_file, index_col=0)
    instances = [Stock(name=item[3], stock_symbol=item[2], isin=item[1], address=item[4], phone=item[5], website=item[6])
                 for item in data_source.itertuples(name=None)]
    Stock.objects.bulk_create(instances)


def get_stock_from_db(ticker, day_range):
    df = pd.DataFrame.from_records(
        DataSource.objects.filter(stock_symbol=ticker.upper()).values_list())
    df = df.rename(columns={1: 'stock_symbol', 2: 'day', 3: 'volume',
                   4: 'stock_open', 5: 'stock_high', 6: 'stock_low', 7: 'stock_close'})
    df = df.drop(columns=[0])
    return df.tail(day_range)


def bollinger_bands(stockname, period):
    df = get_stock_from_db(stockname.upper(), period)
    upper, middle, lower = talib.BBANDS(
        df['stock_close'], timeperiod=20, nbdevup=2,  nbdevdn=2)
    df['upper'] = upper
    df['middle'] = middle
    df['lower'] = lower
    df = df.set_index(df['day'])
    df.dropna(subset=["upper", "middle", "lower"], inplace=True)
    return df


def rsi(stockname, period):
    df = get_stock_from_db(stockname.upper(), period)
    df = df.set_index(df['day'])
    rsi = talib.RSI(df['stock_close'])
    return rsi


def mean_volume(stockname, period):
    df = get_stock_from_db(stockname.upper(), period)
    df['rolling_volume'] = df['volume'].rolling(30).mean().round(4).dropna()
    df2 = df[['day', 'rolling_volume']]
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
        df['rolling_mean'] = df['stock_changes'].rolling(
            5).mean().round(4).dropna()
        df3 = df[['day', 'rolling_mean']].dropna()
        return df3

def convert_to_dataframe(data_set):
    df = pd.DataFrame.from_records(data_set.values_list())
    df = df.rename(columns={1: 'stock_symbol', 2: 'day', 3: 'volume',
                            4: 'stock_open', 5: 'stock_high', 6: 'stock_low', 7: 'stock_close'})
    df = df.drop(columns=[0])
    return df

    
def get_stock_mean_volume_value(ticker, period, end_date):
    """
    Is calculating mean volume value for given stock in given period of time
    Arguments:
        ticker (str):  stock ticker
        period (int): number of days to show
        end_date (str): day till which dataframe should be filtred
    """
    end_date_value = end_date.split("-")
    end_date_converted = datetime(int(end_date_value[0]), int(end_date_value[1]), int(end_date_value[2]))
    data_set = DataSource.objects.filter(stock_symbol=ticker, day__lte = end_date_converted )
    df = convert_to_dataframe(data_set)[-period:]
    df['volumen_value'] = df['stock_close'] * df['volume']
    df = df.groupby(by=['stock_symbol'])['volumen_value'].mean()
    return df



def get_stocks_mean_volumes(period, min_value, end_date):
    """
    Is calculating mean volume value for all stocks in given period of time
    Arguments:
        period (int): number of days to show
        end_date (str): day till which dataframe should be filtred
        min_value (number) : minimal stock volume 
    """
    end_date_value = end_date.split("-")
    end_date_converted = datetime(int(end_date_value[0]), int(end_date_value[1]), int(end_date_value[2]))
    data_set = DataSource.objects.filter(day__range=(end_date_converted - timedelta(period), end_date_converted) ).order_by('stock_symbol')
    df = convert_to_dataframe(data_set)
    df['volumen_value'] = df['stock_close'] * df['volume']
    df = df.groupby(by=['stock_symbol'])['volumen_value'].mean()
    if min_value:
        df = df[df > min_value]
    return df    


def percent_volume_change(ticker, period, end_date):
    """
    Is counting last volume value as percent to mean volume
        Arguments:
        ticker (str):  stock ticker
        period (int): number of days to show
        end_date (str): day till which dataframe should be filtred
    """
    end_date_value = end_date.split("-")
    end_date_converted = datetime(int(end_date_value[0]), int(end_date_value[1]), int(end_date_value[2]))
    data_set = DataSource.objects.filter(stock_symbol= ticker, day__lte = end_date_converted ).last()
    latest_volume_value = data_set.volume * data_set.stock_close
    result = latest_volume_value/get_stock_mean_volume_value(ticker, period,end_date)*100
    return result


def analyze_percent_changes(period, min_value, end_date, range):
    """
    Calculate volmen percent change for all tickers and returns highest change 
        Arguments:
        period (int): number of days to show
        min_value (number) : minimal stock volume 
        end_date (str): day till which dataframe should be filtred
        range (int): number of elements to be returned in dataframe
    """
    mean_values = get_stocks_mean_volumes(period, min_value, end_date)  
    end_date_value = end_date.split("-")
    end_date_converted = datetime(int(end_date_value[0]), int(end_date_value[1]), int(end_date_value[2]))
    last = DataSource.objects.filter(stock_symbol='PKN', day__lte = end_date_converted ).last()
    percent_changes = [{'Date': last.day ,'Ticker':value, 'Change': percent_volume_change(value,period, end_date)[value] } for value in mean_values.index]
    df = pd.DataFrame(percent_changes).sort_values(by=['Change'], ascending=False)
    df = df[df['Date'] >= last.day  ]
    return df[0:range]

def get_key_dates():
    reference = DataSource.objects.filter(stock_symbol='PKN')
    dates = [str(date.day) for date in reference]
    return dates[-30:]

def sma_calculation(period, stockname, dayset):
    """
    Calculate SMA for given stock
        Arguments:
        period (list): list with days values to calculate SMA
        stockname(string): stock ticker
        dayset(int): number of days from which will be calculated SMA.
    """
    results = []
    df = get_stock_from_db(stockname.upper(), dayset)
    df = df.set_index(df['day'])
    for value in period:
        rolling_mean = df['stock_close'].rolling(value).mean().round(4).dropna()
        results.append(rolling_mean)
    return results

def sma_signals(sma_list, names):
    """
    Calculates SMA crossings
        Arguments:
        sma_list(list): list with calculated data from sma_calculation
        names(list): list with sma names
    """
    df = pd.concat([v for v in sma_list], axis=1)
    df.columns = ['sma_'+str(name) for name in names]
    df['next_'+df.columns[0]] = df[df.columns[0]].shift(-1)
    df = df.dropna()
    df[df.columns[0]+'_results']= np.where((df[df.columns[0]] < df[df.columns[1]]) & (df['next_'+df.columns[0]] > df[df.columns[1]]), True, False)
    df =  df[df[df.columns[0]+'_results'] == True]
    return df


def get_tickers():
    """
    Returns all stocks tickers in database
    """
    tickers = Stock.objects.values('stock_symbol')
    ticker_list = [f['stock_symbol'] for f in tickers]
    return ticker_list