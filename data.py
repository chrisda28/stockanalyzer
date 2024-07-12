import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import functools  # used to preserve metadata of function (i.e. function name, docstring)


dotenv_path = os.path.join(os.path.dirname(__file__), 'key.env')   # specifies the path to my environment var
load_dotenv(dotenv_path)  # loading my environment var

API_KEY = os.getenv('apikey')
ENDPOINT = "https://www.alphavantage.co/query"


def api_limit_checker(func):
    call_count = 0
    last_reset = datetime.now()

    @functools.wraps(func)   # used to preserve meta data of function, like name and docstring
    def wrapper(*args, **kwargs):
        nonlocal call_count, last_reset   # gets ahold of variable in one scope outer, so not global
        time_now = datetime.now()   # gets current time

        if time_now - last_reset > timedelta(days=1):  # resetting call count if it's been 1 day
            call_count = 0
            last_reset = time_now
        if call_count >= 25:   # checking if limit has been exceeded
            print("API limit of 25 calls per day exceeded")
            return None   # carried out instead of making an API call

        call_count += 1
        return func(*args, **kwargs)  # calls the original function being decorated
    return wrapper


@api_limit_checker
def get_stock_df(ticker):
    """Makes API call to fetch stock data and returns it as dataframe"""
    parameters = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "outputsize": "full",
            "apikey": API_KEY
        }

    response = requests.get(ENDPOINT, params=parameters)
    response.raise_for_status()    # used for https errors
    json_data = response.json()

    time_series_data = json_data.get("Time Series (Daily)", {})  # getting the time series data into dict
    df = pd.DataFrame.from_dict(time_series_data, orient='index')
    df.index = pd.to_datetime(df.index)   # making sure index treated as datetime
    df = df.astype(float)  # Convert strings to floats
    df.columns = ['open', 'high', 'low', 'close', 'volume']    # setting column names
    df.sort_index(inplace=True)    # sorting the index from oldest at top to the newest on bottom
    return df


@api_limit_checker
def get_multiple_stock_df(tickers):
    """calls get_stock_def() for each ticker and creates dict to map ticker to dataframe"""
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": tickers,
        "outputsize": "full",
        "apikey": API_KEY
    }
    dict_of_all_stock_df = {}
    for ticker in tickers:   # creating dict with key being the ticker and
        # value being the corresponding data frame holding stock data
        time.sleep(16)  # api rate limit respect
        df = get_stock_df(ticker)
        dict_of_all_stock_df[ticker] = df   # setting value to be respective stock's dataframe

    return dict_of_all_stock_df

# if __name__ == "__main__":
#     test_tickers = ["JPM", "GS", "C", "BAC"]
#     try:
#         result = get_multiple_stock_df(test_tickers)
#         print(f"Successfully fetched data for {len(result)} stocks.")
#         for ticker, df in result.items():
#             print(f"{ticker}: {len(df)} rows of data")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")


