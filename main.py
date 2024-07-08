import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'key.env')   # specifies the path to my environment var


load_dotenv(dotenv_path)



api_key = os.getenv('apikey')
print(api_key)

INTERESTED_STOCKS = ["JPM",]  # add more here

parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": INTERESTED_STOCKS,
        "outputsize": "full",
        "apikey": api_key
    }