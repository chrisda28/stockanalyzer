import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'key.env')   # specifies the path to my environment var
load_dotenv(dotenv_path)

api_key = os.getenv('apikey')
INTERESTED_STOCKS = ["JPM", "GS", "BAC", "C"]
endpoint = "https://www.alphavantage.co/query"


def api_call(ticker, api_key):
    parameters = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "outputsize": "full",
            "apikey": api_key
        }

    response = requests.get(endpoint, params=parameters)
    response.raise_for_status()    # used for https errors
    json_data = response.json()
    return json_data


def get_df(json):
    df = pd.DataFrame.from_dict(json['Time Series (Daily)'], orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.astype({   # setting data types for each column
        '1. open': float,
        '2. high': float,
        '3. low': float,
        '4. close': float,
        '5. volume': int
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


data_frame_list = []

for stock in INTERESTED_STOCKS:
    time.sleep(15)
    all_json_data = api_call(stock, api_key)
    all_df = get_df(all_json_data)
    data_frame_list.append(all_df)
