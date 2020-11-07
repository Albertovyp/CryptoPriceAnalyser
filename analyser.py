import pandas as pd
import matplotlib.pyplot as plt


def bar_date_format(series):
    series.index = series.index.map(str)
    counter = 0
    output_list = []
    for i in series.iteritems():
        c = counter
        i = series.index[c]
        i = i[:10]
        counter = counter + 1
        output_list.append(i)

    return output_list


# Get the data from the CSV file to a pandas DataFrame
df = pd.read_csv("/Users/alberto_vega_peralta/PycharmProjects/CryptTrading/Data/IOTA-hour.csv",
                      parse_dates=[0], index_col=['Time'])

# Prompts the user to introduce a timeframe to analyse
print("Introduce the timeframe l you'd like to analyse. \nIf you wish to analyse all the data introduce "
      "0.\n"
      "Data format: YYYY-MM-DD")
start_date = input('Start date: ')
end_date = input('End date: ')

print("Introduce the size of the intervals you wish to analyse for pct_change and volume"
      " Options (hour: H, day: D, month: M, year: Y")
interval = input('Interval: ')

print("Introduce the number of data points you want to display")
data_points = input('Data points: ')
data_points = int(data_points)

# Select to desired timeframe in the pandas DataFrame
if start_date != '0' and end_date != '0':
    mask = (df.index > start_date) & (df.index <= end_date)
    df = df.loc[mask]

# Calculate highest, lowest and average price
highest_price = round(df.High.max(), 3)
lowest_price = round(df.Low.min(), 3)
average_price = round(df.First.mean(), 3)

if interval == 'H' or 'D' or 'M' or 'Y' and data_points > 0:
    # Calculate the interval percentage variation for every datapoint
    change = df.First.pct_change(freq=interval)
    # Add a column with the pct_change to the dataframe
    df["change"] = change
    # Highest price increases
    h = df.change.resample(interval).max().nlargest(data_points)
    h = 100 * h
    # Largest price decreases
    s = df.change.resample(interval).min().nsmallest(data_points)
    s = 100 * s
    # Highest volume
    df = df.astype({'Volume': int})
    v = df.Volume.resample(interval).sum().nlargest(data_points)
else:
    print('You have introduced invalid input')
    exit()

# Calculates simple moving average (SMA)
df['SMA_60'] = df.iloc[:,1].rolling(window=60).mean()

# See info of the Dataframe with all the columns
with pd.option_context('display.max_columns', None):
    print(df.tail())

print('Highest price (USD):', highest_price)
print('Lowest price (USD): ', lowest_price)
print('Average price (USD): ', average_price)

# Plot price and SMA
plt.plot(df['First'], label='Price')
plt.plot(df['SMA_60'], label='Simple Moving average 60 days')
plt.title('Price and Simple Moving Average')
plt.legend(loc='best')
plt.xlabel('Date')
plt.ylabel('Price USD')
plt.show()

# Plot volume
plt.plot(df['Volume'], label='Volume')
plt.title('Volume')
plt.legend(loc='best')
plt.xlabel('Date')
plt.ylabel('USD')
plt.show()

# Plot highest % increases
plt.bar(bar_date_format(h), h)
plt.xticks(rotation=30)
plt.title('Highest price increases')
plt.xlabel('Date')
plt.ylabel('% increase')
x_pos = -0.2
for index, value in h.iteritems():
    value = round(value, 2)
    plt.text(x_pos, value, str(value))
    x_pos = x_pos + 1
plt.show()

# Plot highest % decreases
plt.bar(bar_date_format(s), s)
plt.title('Highest price decreases')
plt.xticks(rotation=30)
plt.xlabel('Date')
plt.ylabel('% decrease')
x_pos = -0.2
for index, value in s.iteritems():
    value = round(value, 2)
    plt.text(x_pos, value, str(value))
    x_pos = x_pos + 1
plt.show()

# Plot highest volume
plt.bar(bar_date_format(v), v)
plt.xticks(rotation=30)
plt.title('Highest volume')
plt.xlabel('Date')
plt.ylabel('USD volume')
plt.show()