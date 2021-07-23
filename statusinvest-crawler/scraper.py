from bs4 import BeautifulSoup
import concurrent.futures
import csv
import json
import psycopg2
import requests
from typing import List

def _tickers_from_db() -> List[str]:
    conn = psycopg2.connect(
        host="env6.lionx.ai",
        database="lionx",
        user="lionx",
        password="FAJvJ4eCVQNexTRL")

    cur = conn.cursor()
    cur.execute("select distinct pk_value from equities;")
    raw_tickers = cur.fetchall()
    return raw_tickers

def _convert_tuple_in_string(tup):
    str = ''
    for item in tup:
        str = str + item
    return str

def _tickers_list():
    raw_tickers = _tickers_from_db()
    tickers = []
    for ticker in raw_tickers:
        ticker = _convert_tuple_in_string(ticker).lower()
        tickers.append(ticker)
    return tickers

print(_tickers_list())

def _build_stock_tickers_urls():
    prefix = 'https://statusinvest.com.br/acoes/'
    urls = []
    for ticker in tickers:
        urls.append(prefix + ticker)






# def build_ticker_urls() -> List[str]:

# dicts = []

# def parse_url():
#     webpage = requests.get(url).content
#     soup = BeautifulSoup(webpage, 'html.parser')



# def getContent(url):
#     try:

#         div = soup.find("div", {"id": "earning-section"})
#         element_input = div.find('input')

#         value = element_input.get('value')
#         value = value.split('},')

#         new_value = []
#         for item in value:
#             new_value.append(item + '}')

#         new_value[-1] = new_value[-1][:-2]
#         new_value[0] = new_value[0][1:]


#         for item in new_value:
#             json_acceptable_string = item.replace("'", "\"")
#             temp = json.loads(json_acceptable_string)
#             new_dict = dict()
#             for (key, value) in temp.items():
#                 if key == 'ed' or key == 'pd' or key == 'et' or key == 'v':
#                     new_dict[key] = value
#             new_dict['ticker'] = url.split('/')[-1]
#             dicts.append(new_dict)
#         print(url)
#     except:
#         print('Error in ' + url)

