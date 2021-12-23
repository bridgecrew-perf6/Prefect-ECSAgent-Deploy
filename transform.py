import pandas as pd
import numpy as np
from extract import get_exchange_rate

pd.set_option('display.float_format', '{:.10f}'.format)
pd.set_option('display.max_colwidth', -1)

def add_full_link(dataframe):
    base_link = "https://coinmarketcap.com"
    dataframe['Href'] = dataframe['Href'].apply([lambda x: base_link + x])
    return dataframe

def convert_to_float(dataframe, column):
    try: 
        dataframe[column] = dataframe[column].astype(float)
    except ValueError as e:
        error_price = str(e).split("'")[1]
        dataframe.loc[dataframe[column] == error_price, [column]] = 0.000000002131
    return dataframe

def convert_to_int(dataframe, column):
    dataframe[column] = dataframe[column].apply([lambda x : x.replace(',','')]).astype(int)
    return dataframe

def convert_to_aud(dataframe):
    exchange_rate = get_exchange_rate()
    dataframe['Price'] = dataframe['Price'].astype(float)
    dataframe[['Price', 'Volume']] = dataframe[['Price', 'Volume']]*exchange_rate
    return dataframe


def transform_data(dataframe):
    dataframe = add_full_link(dataframe)
    dataframe = convert_to_float(dataframe, 'Price')
    dataframe = convert_to_int(dataframe, 'Volume')
    dataframe = convert_to_aud(dataframe)
    return dataframe
