import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'key.env')   # specifies the path to my environment var
load_dotenv(dotenv_path)

api_key = os.getenv('apikey')
INTERESTED_STOCKS = ["JPM",]  # add more here
endpoint = "https://www.alphavantage.co/query"

parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": INTERESTED_STOCKS,
        "outputsize": "full",
        "apikey": api_key
    }

response = requests.get(endpoint, params=parameters)
response.raise_for_status()    # used for https errors
json_data = response.json()

df = pd.DataFrame.from_dict(json_data)
# df.rename(columns={})
trimmed_top_rows = df.iloc[5:] # deletes the first 5 rows
deleted_column_one = trimmed_top_rows.iloc[:, 1:]  # deletes meta data column
final_df = deleted_column_one.rename(columns={"Time Series (Daily)": "JPM Daily Time Series"})  # rename column
print(final_df)
