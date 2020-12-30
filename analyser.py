import pandas as pd
from ta.momentum import RSIIndicator
from ta.volume import MFIIndicator
import openpyxl


# Add a column with the percentage change of the given interval
def pct_change(frame, interval):
    change = frame.Last.pct_change(freq=interval)
    frame['change'] = change
    return frame


def typical_price(frame):
    typ_price = (frame['High'] + frame['Low'] + frame['Last']) / 3
    frame['Typical'] = typ_price
    return frame


def highest_price(frame):
    highest_price = round(frame.High.max(), 3)
    return highest_price


def lowest_price(frame):
    lowest_price = round(frame.Low.min(), 3)
    return lowest_price


def average_price(frame):
    average_price = round(frame.Typical.mean(), 3)
    return average_price


def biggest_up_movements(frame, interval, number_of_movements):
    h = frame.change.resample(interval).max().nlargest(number_of_movements)
    return h


def biggest_drawdowns(frame, interval, number_of_movements):
    s = frame.change.resample(interval).min().nsmallest(number_of_movements)
    return s


def biggest_volume(frame, interval, data_points):
    v = frame.Volume.resample(interval).sum().nlargest(data_points)
    return v


def lowest_volume(frame, interval, data_points):
    v = frame.Volume.resample(interval).sum().nsmallest(data_points)
    return v


def volatility(frame):
    daily_volatility = frame.change.resample('D').mean().std()
    annualized_volatility = daily_volatility * (356 ** (1/2))
    return [daily_volatility, annualized_volatility]


def simple_moving_average(frame, window):
    frame['SMA' + str(window)] = df.iloc[:, 1].rolling(window=window).mean()
    return frame


def rsi_indicator(daily_frame):
    indicator_RSI = RSIIndicator(close=daily_frame['Last'])
    daily_frame['RSI'] = indicator_RSI.rsi()
    return daily_frame


def money_flow_index(daily_frame):
    indicator_MFI = MFIIndicator(high=daily_frame['High'], low=daily_frame['Low'], close=daily_frame['Last'],
                                 volume=daily_frame['Volume'])
    daily_frame['MFI'] = indicator_MFI.money_flow_index()
    return daily_frame


def simple_moving_average(daily_frame, window):
    daily_frame['SMA' + str(window)] = daily_frame['Typical'].rolling(window=window).mean()
    return daily_frame


def correlation(frame, asset2_frame):
    typical_price(frame)
    typical_price(asset2_frame)
    asset1 = frame['Typical']
    asset2 = asset2_frame['Typical']
    corr = asset1.corr(asset2)
    return corr


# Get the data from the CSV file to a pandas DataFrame
df = pd.read_csv("FilePath", parse_dates=[0], index_col=['Time'])


df2 = pd.read_csv("FilePath", parse_dates=[0], index_col=['Time'])

# Prompts the user to introduce a timeframe to analyse
print("Introduce the timeframe you'd like to analyse. \nIf you wish to analyse all the data introduce "
      "0.\n"
      "Data format: YYYY-MM-DD")
start_date = input('Start date: ')
end_date = input('End date: ')

# Select to desired timeframe in the pandas DataFrame
if start_date != '0' and end_date != '0':
    mask = (df.index > start_date) & (df.index <= end_date)
    df = df.loc[mask]

# Creates a frame with daily data
day_df = df.resample('D').last()
day_df['First'] = df['First'].resample('D').first()
day_df['High'] = df['High'].resample('D').max()
day_df['Low'] = df['Low'].resample('D').min()
day_df['Volume'] = df['Volume'].resample('D').sum()


# Examples
pct_change(df, 'D')
typical_price(df)
typical_price(day_df)
volatility(df)
rsi_indicator(day_df)
money_flow_index(day_df)
simple_moving_average(day_df, 60)
print(correlation(df, df2))
print('Highest price (USD):', highest_price(df))
print('Lowest price (USD): ', lowest_price(df))
print('Average price (USD): ', average_price(df))
print('Daily volatility:', volatility(df)[0])
print('Volatility:', volatility(df)[1])


# See info of the Dataframe with all the columns
with pd.option_context('display.max_columns', None):
    print(df.head())
    print(df.tail())
    print(day_df.head())
    print(day_df.tail())


# Import to excel
with pd.ExcelWriter('CryptoPriceData.xlsx', mode='a') as writer:
    df['Last'].resample('D').last().to_excel(writer, sheet_name='Last_Price')
    day_df.to_excel(writer, sheet_name='Daily Data Frame')
