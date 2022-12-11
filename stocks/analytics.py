import pandas as pd
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


def stocks_files_paths(dir):
    file_list = list(pathlib.Path(dir).glob('*.txt'))
    return file_list

def read_mean_volumen():
    df = pd.DataFrame.from_records(DayList.objects.filter(option = 'V').values_list())
    df = df.drop(columns=[0,4,5])
    df = df.rename(columns={1: 'option', 2: 'day', 3: 'stock_symbol',6: 'percent_change'})
    df = df.sort_values(by=['percent_change'], ascending=False)
    print(df)


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
def update_database():
    PATH = r"C:\\Users\\lukaa\Desktop\\d_pl_txt\\data\\daily\\pl\\wse stocks\\"
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
        DataSource.objects.filter(stock_symbol=ticker).values_list())
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

def get_last_data_entry(ticker):
    data_set = DataSource.objects.filter(stock_symbol=ticker)
    return data_set.last()


def convert_to_dataframe(data_set):
    df = pd.DataFrame.from_records(data_set.values_list())
    df = df.rename(columns={1: 'stock_symbol', 2: 'day', 3: 'volume',
                            4: 'stock_open', 5: 'stock_high', 6: 'stock_low', 7: 'stock_close'})
    df = df.drop(columns=[0])
    return df

def get_stock_mean_volume_value(ticker, period):
    data_set = DataSource.objects.filter(stock_symbol=ticker)
    df = convert_to_dataframe(data_set)[-period:]
    df['volumen_value'] = df['stock_close'] * df['volume']
    df = df.groupby(by=['stock_symbol'])['volumen_value'].mean()
    return df


def get_stocks_mean_volumes(period, min_value):
    time_difference = get_last_data_entry('PKN').day - timedelta(days=period)
    data_set = DataSource.objects.filter(
        day__gte=time_difference).order_by('stock_symbol')
    df = convert_to_dataframe(data_set)
    df['volumen_value'] = df['stock_close'] * df['volume']
    df = df.groupby(by=['stock_symbol'])['volumen_value'].mean()
    if min_value:
        df = df[df > min_value]
    return df

# Is counting last volume value as percent to mean volume
def percent_volume_change(ticker, period):
    latest_volume_value = get_last_data_entry(
        ticker).volume * get_last_data_entry(ticker).stock_close
    return latest_volume_value/get_stock_mean_volume_value(ticker, period)*100

# Calculate volumne percent change for all tickers and returns highest change 
def analyze_percent_changes(period, min_value, range):
    mean_values = get_stocks_mean_volumes(period, min_value)  
    percent_changes = [{'Date': get_last_data_entry(value).day ,'Ticker':value, 'Change': percent_volume_change(value,period)[value] } for value in mean_values.index]
    df = pd.DataFrame(percent_changes).sort_values(by=['Change'], ascending=False)
    df = df[df['Date'] >= get_last_data_entry('PKN').day]
    return df[0:range]
