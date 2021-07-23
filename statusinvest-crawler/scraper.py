from bs4 import BeautifulSoup
import concurrent.futures
import csv
import json
# import psycopg2
import requests

# conn = psycopg2.connect(
#     host="env6.lionx.ai",
#     database="lionx",
#     user="lionx",
#     password="FAJvJ4eCVQNexTRL")

# cur = conn.cursor()
# cur.execute("select distinct pk_value from equities union select distinct symbol from etf;")
# raw_tickers = cur.fetchall()



def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
    return str

tickers = []
for ticker in raw_tickers:
    ticker = convertTuple(ticker).lower()
    tickers.append(ticker)

prefix = 'https://statusinvest.com.br/acoes/'
urls = []
for ticker in tickers:
    urls.append(prefix + ticker)

dicts = []


def getContent(url):
    try:
        webpage = requests.get(url).content
        soup = BeautifulSoup(webpage, 'html.parser')

        div = soup.find("div", {"id": "earning-section"})
        element_input = div.find('input')

        value = element_input.get('value')
        value = value.split('},')

        new_value = []
        for item in value:
            new_value.append(item + '}')

        new_value[-1] = new_value[-1][:-2]
        new_value[0] = new_value[0][1:]


        for item in new_value:
            json_acceptable_string = item.replace("'", "\"")
            temp = json.loads(json_acceptable_string)
            new_dict = dict()
            for (key, value) in temp.items():
                if key == 'ed' or key == 'pd' or key == 'et' or key == 'v':
                    new_dict[key] = value
            new_dict['ticker'] = url.split('/')[-1]
            dicts.append(new_dict)
        print(url)
    except:
        print('Error in ' + url)

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     executor.map(getContent, urls)


# keys = dicts[0].keys()
# with open('results.csv', 'a', newline='')  as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(dicts)
