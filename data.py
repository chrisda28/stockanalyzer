import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), 'key.env')   # specifies the path to my environment var
load_dotenv(dotenv_path)  # loading my environment var

api_key = os.getenv('apikey')
INTERESTED_STOCKS = ["JPM", "GS", "BAC", "C"]
ENDPOINT = "https://www.alphavantage.co/query"


def api_call(ticker, api_key):
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
    return json_data


def get_df(json):
    """converts json data to cleaned dataframe"""
    df = pd.DataFrame.from_dict(json['Time Series (Daily)'], orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.astype({   # setting data types for each column
        '1. open': float,
        '2. high': float,
        '3. low': float,
        '4. close': float,
        '5. volume': 'int64'  # changed from int
    })
    df = df.rename(columns={  # improving column names
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    })
    df = df.sort_index()
    return df


def final_stock_data(stocks, api_key):
    """gathers data frames for each stock into a list"""
    data_frame_list = []
    for stock in stocks:
        time.sleep(15)  # considering API rate limits
        json_data = api_call(stock, api_key)  # get ahold of json data
        df = get_df(json_data)  # get ahold of data frame
        df['ticker'] = stock  # Add ticker column
        data_frame_list.append(df)  # put dataframe into the list
    return data_frame_list


if __name__ == "__main__":
    stock_data = final_stock_data(INTERESTED_STOCKS, api_key)  # gets ahold of list of data frames
    print(f"Fetched data for {len(stock_data)} stocks")

    for i, df in enumerate(stock_data):
        df.to_csv(f"stock_data_{INTERESTED_STOCKS[i]}")   # saves each data frame into a csv file and makes file name
    print("Data saved into CSV files.")


