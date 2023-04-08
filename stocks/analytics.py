import pandas as pd
import numpy as np
from .models import DataSource, Stock, DayList
import datetime
import talib
import pathlib
from datetime import timedelta, datetime, date
from talib import abstract
from .candlesNames import candle_name_table


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
def add_daylist_to_db(df, option):
    if option == 'V':
        instances = [DayList.objects.create(option='V', day=stock['Date'], stock_symbol=Stock.objects.get(
            stock_symbol=stock['Ticker']), volume=stock['Change']) for i, stock in df.iterrows()]
        DayList.objects.bulk_create(instances)
    if option == 'M':
        instances = [DayList.objects.create(option='M', day=stock['Date'], stock_symbol=Stock.objects.get(
            stock_symbol=stock['Ticker']), mean=stock['Change']) for i, stock in df.iterrows()]
        DayList.objects.bulk_create(instances)
    if option == 'C':
        instances = [DayList.objects.create(option='C', day=stock['Date'], stock_symbol=Stock.objects.get(
            stock_symbol=stock['Ticker']), candle=stock['Change']) for i, stock in df.iterrows()]
        DayList.objects.bulk_create(instances)


def stocks_files_paths(dir):
    file_list = list(pathlib.Path(dir).glob('*.txt'))
    return file_list


def read_daylist(db_option):
    """
    Is reading data from DayList database
    Arguments:
        db_option (str):  option base on which input is filtred.
    """
    df = pd.DataFrame.from_records(
        DayList.objects.filter(option=db_option).values_list())
    if db_option == 'V':
        df = df.drop(columns=[0, 4, 5])
        df = df.rename(columns={1: 'option', 2: 'day',
                       3: 'stock_symbol', 6: 'percent_change'})
    if db_option == 'M':
        df = df.drop(columns=[0, 4, 6])
        df = df.rename(columns={1: 'option', 2: 'day',
                       3: 'stock_symbol', 5: 'crossing'})
    if db_option == 'C':
        df = df.drop(columns=[0, 5, 6])
        df = df.rename(columns={1: 'option', 2: 'day',
                       3: 'stock_symbol', 4: 'candles'})
    df = df.groupby(by=['day'])
    return df

# Is adding missing stocks details to database, which were not importet correctly by scrapping


def add_missing_stock_data():
    PATH = r'D:\\dev\\Scrapping\\danespolek.txt'
    df = pd.read_csv(PATH)
    database = [v.stock_symbol for v in Stock.objects.all()]
    instances = []
    for i, item in df.iterrows():
        if item['stock_symbol'] not in database:
            instances.append(Stock(name=item['name'], stock_symbol=item['stock_symbol'], isin=item['isin'],
                             address=item['address'], phone=item['phone'], website=item['website']))
    Stock.objects.bulk_create(instances)
    print("dodane")

# Update database base on new daily stock data


def update_database(option):
    PATH = ''
    if option == 'wse':
        PATH_WSE = r"C:\\Users\\lukaa\Desktop\\d_pl_txt\\data\\daily\\pl\\wse stocks\\"
        PATH = PATH_WSE
    if option == 'nc':
        PATH_NC = r"C:\\Users\\lukaa\Desktop\\d_pl_txt\\data\\daily\\pl\\nc stocks\\"
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
                        print(
                            new_stock_data['<TICKER>'], new_stock_data['<DATE>'], "Stock data added")
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
    end_date_converted = datetime(int(end_date_value[0]), int(
        end_date_value[1]), int(end_date_value[2]))
    data_set = DataSource.objects.filter(
        stock_symbol=ticker, day__lte=end_date_converted)
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
    end_date_converted = datetime(int(end_date_value[0]), int(
        end_date_value[1]), int(end_date_value[2]))
    data_set = DataSource.objects.filter(day__range=(
        end_date_converted - timedelta(period), end_date_converted)).order_by('stock_symbol')
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
    end_date_converted = datetime(int(end_date_value[0]), int(
        end_date_value[1]), int(end_date_value[2]))
    data_set = DataSource.objects.filter(
        stock_symbol=ticker, day__lte=end_date_converted).last()
    latest_volume_value = data_set.volume * data_set.stock_close
    result = latest_volume_value / \
        get_stock_mean_volume_value(ticker, period, end_date)*100
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
    end_date_converted = datetime(int(end_date_value[0]), int(
        end_date_value[1]), int(end_date_value[2]))
    last = DataSource.objects.filter(
        stock_symbol='PKN', day__lte=end_date_converted).last()
    percent_changes = [{'Date': last.day, 'Ticker': value, 'Change': percent_volume_change(
        value, period, end_date)[value]} for value in mean_values.index]
    df = pd.DataFrame(percent_changes).sort_values(
        by=['Change'], ascending=False)
    df = df[df['Date'] >= last.day]
    return df[0:range]


def get_key_dates(period):
    """
    Return dates based on databse input.
        Arguments:
        period(int): Number of entries to return 
    """
    reference = DataSource.objects.filter(stock_symbol='PKN')
    dates = [str(date.day) for date in reference]
    return dates[-period:]


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
        rolling_mean = df['stock_close'].rolling(
            value).mean().round(4).dropna()
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
    df[df.columns[0]+'_results_up'] = np.where((df[df.columns[0]] < df[df.columns[1]]) & (
        df['next_'+df.columns[0]] > df[df.columns[1]]), True, False)
    df[df.columns[0]+'_results_down'] = np.where((df[df.columns[0]] > df[df.columns[1]]) & (
        df['next_'+df.columns[0]] < df[df.columns[1]]), True, False)
    df_up = df[df[df.columns[0]+'_results_up'] == True]
    df_down = df[df[df.columns[0]+'_results_down'] == True]
    return df_up, df_down


def get_tickers():
    """
    Returns all stocks tickers in database
    """
    tickers = Stock.objects.values('stock_symbol')
    ticker_list = [f['stock_symbol'] for f in tickers]
    return ticker_list


def add_sma_crossings_to_db(sma1, sma2, dayset):
    """
    Is adding sma crossings results to database.
        Arguments:
        sma_1(int): first sma , must be lower than sma2
        sma_2(int): second sma, must be higher than sma1
        dayset(int): number of days from which will be calculated SMA.
    """
    results = []
    tickers = get_tickers()
    for t in tickers:
        try:
            sma = sma_calculation([sma1, sma2], t, dayset)
            signals_up = sma_signals(sma, [sma1, sma2])[0]
            signals_down = sma_signals(sma, [sma1, sma2])[1]
            signals_up['ticker'] = t
            signals_down['ticker'] = t
            results.append(signals_up)
            results.append(signals_down)
        except:
            print("error " + t)
    df = pd.concat(results)
    df = df.sort_index(ascending=False)
    d_data = []
    for v in df.iterrows():
        d_data.append([v[0], v[1][5], df.columns[0]+" "+df.columns[1]+" "+str(v[1]
                      [df.columns[0]+'_results_up'])+" "+str(v[1][df.columns[0]+'_results_down'])])
    df_db = pd.DataFrame(d_data, columns=['Date', 'Ticker', 'Change'])
    add_daylist_to_db(df_db, 'M')


def rename_candles_to_db(df):
    """
    Is adding candle patterns for given ticker to database
        Arguments:
        df(DataFrame): DataFrame with candles patterns
    """
    df = df.rename(columns={"stock_symbol": "Ticker",
                   "day": "Date", "candle": "Change"})
    return df


def get_sma_results_from_db():
    """
    Reads sma data from database. 
    """
    sma_data = pd.DataFrame.from_records(
        DayList.objects.filter(option='M').values_list())
    sma_data = sma_data.drop([0, 1, 4, 6], axis=1)
    sma_data = sma_data.rename(columns={2: "Date", 3: "Ticker", 5: "Crossing"})
    return sma_data


def sma_template_data(df, sma1, sma2):
    """
    It Converts data from database to data for template
        Arguments:
        df(DataFrame): dataframe with sma data. 
        sma1(stiring): first smaller sma
        sma2(sting): second bigger sma
    """
    t = df.iterrows()
    results = []
    for v in t:
        crossing_data = v[1]['Crossing'].split(" ")
        if (sma1 == crossing_data[0] and sma2 == crossing_data[1]):
            results.append({'Date': str(v[1]["Date"]), 'Ticker': v[1]['Ticker'], 'SMA1': crossing_data[0],
                           'SMA2': crossing_data[1], 'UP': crossing_data[2], 'DOWN': crossing_data[3]})
    return results


def sma_elements(date):
    """
    Returns sma crossings data based on given dates.
        Arguments:
        date(List): list with dates of sma crossings.
    """
    results = []
    df = get_sma_results_from_db()
    df = df.groupby(by=['Date'])
    for crossing_date, sma_data in df:
        for value in date:
            if crossing_date == datetime.strptime(str(value), '%Y-%m-%d').date():
                results.append(sma_data)
    new_df = pd.concat(results).iloc[::-1]
    return new_df


def get_unique_dates(list):
    return sorted(set(list), reverse=True)


def get_crossing_dates(crossing_data):
    """
    Return dates for sma crossing.
        Arguments:
        crossing_data(DataFrame): result of read_daylist function.
    """
    sma_15_45_dates = []
    sma_50_200_dates = []
    for v, p in crossing_data:
        if "sma_15" in p['crossing'].values[0].split(" "):
            sma_15_45_dates.append(str(v))
        if "sma_45" in p['crossing'].values[0].split(" "):
            sma_50_200_dates.append(str(v))
    return sma_15_45_dates, sma_50_200_dates


def candle_pattern(ticker, period):
    """
    Returns candle patterns based on given timeframe
        Arguments:
        ticker (str):  stock ticker
        period (int): number of days to show
    """
    result = pd.DataFrame(columns=['stock_symbol', 'day', 'candle', 'direction'])
    candle_name = talib.get_function_groups()['Pattern Recognition']
    df = get_stock_from_db(ticker, period)
    df.rename(columns={'stock_open': 'open', 'stock_high': 'high',
              'stock_low': 'low', 'stock_close': 'close'}, inplace=True)
    for indicator in candle_name:
        df[str(indicator)] = getattr(abstract, indicator)(df)
    for indicator in candle_name:
        if (df[str(indicator)] == 0).all():
            df = df.drop([indicator], axis=1)
    for pattern in df.columns[7:]:
        candle_table = df.loc[df[pattern].where(
            df[pattern] != 0).dropna().index]
        candle_table['candle'] = pattern
        candle_table['direction'] = candle_table[pattern]
        candle_table.loc[candle_table['direction'] > 0 , 'candle_direction' ] = candle_table['candle'] + "_UP"
        candle_table.loc[candle_table['direction'] < 0 , 'candle_direction' ] = candle_table['candle'] + "_DOWN"
        result = pd.concat(
            [result, candle_table[['stock_symbol', 'day', 'candle','direction', 'candle_direction']]])
    result = result.drop(['candle'], axis= 1)
    result = result.rename(columns = {'candle_direction':'candle'})
    result = result.drop(['direction'], axis= 1)
    return result


def add_candle_data_to_db(period):
    """
    Is adding candle pattern data to database
        Arguments:
        period (int): number of days to add
    """
    result_data = []
    for ticker in get_tickers():
        print(ticker)
        patterns = candle_pattern(ticker, period)
        result_data.append(patterns)

    t = pd.concat(result_data, ignore_index=True)
    add_daylist_to_db(rename_candles_to_db(t), 'C')
