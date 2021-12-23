import pandas as pd
import numpy as np
from extract import get_exchange_rate

# setting float and column width parameters
pd.set_option('display.float_format', '{:.10f}'.format)
pd.set_option('display.max_colwidth', -1)

# the function below appends "https://coinmarketcap.com" to every crypto pair.
# this makes it a weblink, where more information can be gathered regarding cypto pair.
def add_full_link(dataframe):
    base_link = "https://coinmarketcap.com"
    dataframe['Href'] = dataframe['Href'].apply([lambda x: base_link + x])
    return dataframe

# the function below converts scrapped text in string format into float - use for price
def convert_to_float(dataframe, column):
    try: 
        dataframe[column] = dataframe[column].astype(float)
    except ValueError as e:
        error_price = str(e).split("'")[1]
        dataframe.loc[dataframe[column] == error_price, [column]] = 0.000000002131
    return dataframe

# the function below converts scrapped text in string format into integer - use for volume
def convert_to_int(dataframe, column):
    dataframe[column] = dataframe[column].apply([lambda x : x.replace(',','')]).astype(int)
    return dataframe

# the function use scrapped AUD/USD exchange rate to convert USD into AUD
def convert_to_aud(dataframe):
    exchange_rate = get_exchange_rate()
    dataframe['Price'] = dataframe['Price'].astype(float)
    dataframe[['Price', 'Volume']] = dataframe[['Price', 'Volume']]*exchange_rate
    return dataframe

# the function execute all the above functions to return a transformed dataframe
def transform_data(dataframe):
    dataframe = add_full_link(dataframe)
    dataframe = convert_to_float(dataframe, 'Price')
    dataframe = convert_to_int(dataframe, 'Volume')
    dataframe = convert_to_aud(dataframe)
    return dataframe
