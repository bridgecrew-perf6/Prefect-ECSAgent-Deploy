import requests
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_colwidth', -1)
pd.set_option('display.float_format', '{:.10f}'.format)

def top_gainers_today():
    # coin martket cap for top gainers and loser, updated everyday
    URL = "https://coinmarketcap.com/gainers-losers/"

    # using request to fetch html
    r = requests.get(URL)

    # making a Soup object and finding the top gainers table
    soup = BeautifulSoup(r.content, 'html5lib')
    gainers_table = soup.find('div', class_ = 'h7vnx2-1 gDdiUn').find('tbody')
    
    # scrapping symbol, prince, percentage gain and volume
    gainers = []
    for crypto in gainers_table.findAll('tr'):
        name = crypto.find('p', class_='sc-1eb5slv-0 iworPT').text
        symbol = crypto.find('p', class_='sc-1eb5slv-0 gGIpIK coin-item-symbol').text
        price = crypto.find('span').text[1:]
        gain = crypto.find('span', class_='sc-15yy2pl-0 kAXKAX').text[:-1]
        volume = crypto.findAll('td', style='text-align:right')[-1].text[1:]
        href_ = str(crypto.find('a', class_='cmc-link')['href'])
        gainers.append([name, symbol, price, gain, volume, href_])
        
    # creating and returning Dataframe    
    top_gainers = pd.DataFrame(gainers, columns = ['Name', 'Symbol', 'Price', 'Gain_Percentage', 'Volume', 'Href'])
    return top_gainers

def get_exchange_rate():
    URL = 'https://wise.com/au/currency-converter/usd-to-aud-rate'
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    exchange_rate = soup.find('span', class_='text-success').text
    exchange_rate = float(exchange_rate)
    return exchange_rate
