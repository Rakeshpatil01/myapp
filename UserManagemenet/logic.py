import re
import numpy as np  # linear algebra
import pandas as pd  # pandas for dataframe based data processing and CSV file I/O
import requests
import time
from datetime import datetime


def convert_to_datetimestamp(given_date):
    """
        converts datetime to timestamp unix
    """
    time_tuple = given_date.timetuple()
    timestamp = round(time.mktime(time_tuple))
    return timestamp


def convert_to_datetime(given_date):
    """
        converts timestamp unix to datetime
    """
    return datetime.fromtimestamp(given_date)


def history_data(symbol, interval, start_timestamp, end_timestamp):
    start_timestamp = convert_to_datetimestamp(start_timestamp)
    end_timestamp = convert_to_datetimestamp(end_timestamp)
    interval = interval
    symbol = symbol
    url = f"https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol={symbol}&resolution={interval}&from={start_timestamp}&to={end_timestamp}"
    req = requests.get(url).json()
    df = pd.DataFrame(req)
    df['t'] = df['t'].apply(lambda x: convert_to_datetime(x))
    df.drop(columns=['s'], inplace=True)
    df.rename(columns={"h": "High", "l": "Low",
              "c": "Close", "o": "Open", "v": "Volume", "t": "Date"}, inplace=True)
    req = df.to_dict("records")
    return req
