import datetime
import bitfinex
import time
import pandas as pd


def fetch_data(start, stop, symbol, interval, tick_limit, step):
    # Create api instance
    api_v2 = bitfinex.bitfinex_v2.api_v2()
    data = []
    start = start -step
    while start < stop:
        start = start + step
        end = start + step
        res = api_v2.candles(symbol=symbol, interval=interval,
                             limit=tick_limit, start=start, end=end)
        data.extend(res)
        time.sleep(2)
    return data


# Set step size
time_step = 60000000

# Define query parameters
pair = 'iotusd'  # Currency pair of interest
bin_size = '1h'  # This will return minute, hour or day data
limit = 1000  # We want the maximum of 1000 data points
# Define the start date
t_start = datetime.datetime(2020, 8, 13, 0, 0)
t_start = time.mktime(t_start.timetuple()) * 1000
# Define the end date
t_stop = datetime.datetime(2020, 8, 14, 0, 0)
t_stop = time.mktime(t_stop.timetuple()) * 1000
result = fetch_data(start=t_start, stop=t_stop, symbol=pair, interval=bin_size, tick_limit=limit, step=time_step)

# Converts the timestamp into readable datetime info

# Creates a pandas dataframe to store the results from the query
df = pd.DataFrame(result, columns=['Time', 'First', 'Last',
                                'High', 'Low', 'Volume'])
df.drop_duplicates(inplace=True)
df['Time'] = pd.to_datetime(df['Time'], unit='ms')
df.set_index('Time', inplace=True)
df.sort_index(inplace=True)
# Imports the data into a csv file
df.to_csv("file_path")
