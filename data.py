import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), 'key.env')   # specifies the path to my environment var
load_dotenv(dotenv_path)  # loading my environment var

api_key = os.getenv('apikey')
ENDPOINT = "https://www.alphavantage.co/query"


def get_stock_df(ticker):
    """Make API call to fetch stock data and returns it as json data"""
    parameters = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "outputsize": "full",
            "apikey": api_key
        }

    response = requests.get(ENDPOINT, params=parameters)
    response.raise_for_status()    # used for https errors
    json_data = response.json()

    time_series_data = json_data.get("Time Series (Daily)", {})  # getting the time series data into dict
    df = pd.DataFrame.from_dict(time_series_data, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)  # Convert strings to floats
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.sort_index(inplace=True)
    return df


def get_multiple_stock_df(tickers):
    """converts json data to cleaned dataframe"""
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": tickers,
        "outputsize": "full",
        "apikey": api_key
    }
    dict_of_all_stock_df = {ticker: get_stock_df(tickers) for ticker in tickers}  # creating dict with key being the
    # ticker and value being the corresponding data frame holding stock data
    return dict_of_all_stock_df





