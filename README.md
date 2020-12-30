# CryptoPriceAnalyser
Import cryptocurrency historical price data from Btifinex API, store it in a csv file and perform basic analysis over it.
This project consists of two scripts: an importer and an analyser.

## import.py
This code comes from the Bitfinex API documentation (https://docs.bitfinex.com/docs) and from a blogpost from Carsten Klein, an engenieer from Bitfinex (https://medium.com/coinmonks/how-to-get-historical-crypto-currency-data-954062d40d2d). My adittions are a few lines of code to export the DataFrame to a new csv and to update an existing csv file. Make sure to follow the steps of the Bitfinex API docs to set up the connection to the API correctly.
 - Asks the user whether he wants to create a csv file or update an existing one. 
 - Connects to the Bitfinex API and gets the desiried data. The user can specify:
    - Cryptocurrency ticker.
    - Granularity of the data (minute, hour, day...). 
    - Timeframe.
 - Transforms the output of the query (a list of lists) containing the data into a pandas dataframe to facilitate the analysis.
 - Writes the pandas DataFrame into a csv file.
 
## analyser.py
- Reads a csv file with the time-series data and transforms it into a pandas Dataframe.
- Asks the user for input about the desired period to analyse.
- Provides a set of functions that abstract the sintax of the pandas library and calculates various metrics. The functions can be used to calculate: percentage change between different data points, typical price, highest price, lowest price, average price, biggest up movements, biggest drawdowns, biggest volumes, lowest volumes, correlation and volatility.
- Provides functions to calculate technical indicators that might be useful to spot overbought and oversold situations. The indicators are: Simple Moving Averages, the Relative Strength Indicator and the Money Flow Index (The latter two functions are just abstractions of the ta library developed by bukosabino https://github.com/bukosabino/ta). 
