# CryptoPriceAnalyser
Import cryptocurrency historical price data from Btifinex api, store it in a csv file and perform basic analysis over it.
This project consists of two programs: an importer and an analyser.

## import.py
This code comes from the Bitfinex API documentation (https://docs.bitfinex.com/docs) and from a blogpost from a bitfinex engenieer (https://medium.com/coinmonks/how-to-get-historical-crypto-currency-data-954062d40d2d). My only adittion has been a line of code to export the DataFrame into a csv file. Make sure to follow the steps of the Bitfinex API docs to set up the connection to the API correctly.

 - Connects to the Bitfinex api and gets the desiried data. The user can specify:
    - Cryptocurrency ticker.
    - Granularity of the data (minute, hour, day...).
    - Timeframe.
 - Transforms the output of the query (a list of lists) containing the data into a pandas dataframe to facilitate the analysis.
 - Writes the pandas DataFrame into a csv file.
 
## analyser.py
- Reads a csv file with the data and transforms it into a pandas Dataframe.
- Asks the user for input about the desired period to analyse.
- Calculates top N percentage price increases and decreases and top N volumes of the period using the specified time interval. The user can specify:
    - N.
    - The time interval. The available time intervals are hours (H), days(D), months(M) and years(Y)
- Calculates a Simple Moving Average (SMA).
- Plots the following graphs.
    - Representation of the price and the SMA.
    - Representation of the historical volume
    - Representation of the top N % price increases using the given time interval.
    - Representation of the top N % price decreases using the given time interval.
    - Representation of the top N volumes using the given time interval.
