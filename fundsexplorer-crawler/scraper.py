import requests
from bs4 import BeautifulSoup
import json
import csv
import concurrent.futures

# Enquanto não temos os FII's separados no banco de dados e os ETF's de renda fixa, utilizaremos um array com esses ativos
funds = ['abcp11', 'afcr11']

tickers = []
# for ticker in funds:
#     ticker = ticker.lower()
#     tickers.append(ticker)

prefix = 'https://www.fundsexplorer.com.br/funds/'
urls = []
for ticker in funds:
    urls.append(prefix + ticker)

dicts = []
def getData(url):
    try:
        webpage = requests.get(url).content
        soup = BeautifulSoup(webpage, 'html.parser')

        # fii - Dividend Yield
        fii_section = soup.find("section", {"id": "dividends"})
        fii_table = fii_section.find('table')
        fii_tr = fii_table.find_all('tr')[-1]
        fii_td = fii_tr.find_all('td')
        td_dividend_yield_last_year = fii_td[-2].text
        td_dividend_yield_last_month = fii_td[1].text

        # Taxas de Administração e Performance
        taxas_section = soup.find("section", {"id": "basic-infos"})
        taxas_li = taxas_section.find_all('li')

        # Taxa de performance
        taxas_li_performance = taxas_li[6]
        fii_performance = taxas_li_performance.text.strip()
        text_perfomance = " ".join(fii_performance.split()).split('performance')[1].strip()


        # Taxa de adm
        taxas_li_administracao = taxas_li[-3]
        fii_administracao = taxas_li_administracao.text.strip()
        text_administracao = " ".join(fii_administracao.split()).split('administração')[1].strip()


        # Criação de dicionário
        new_dict = dict()

        new_dict['taxa de performance'] = text_perfomance
        new_dict['taxa de administração'] = text_administracao
        new_dict['Last Month Dividend Yield'] = td_dividend_yield_last_month
        new_dict['Last Year Dividend Yield'] = td_dividend_yield_last_year

        dicts.append(new_dict)
        print(url)
    except:
        print('Error: ' + url)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(getData, urls)

keys = dicts[0].keys()
with open('fundsExplorer.csv', 'a', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(dicts)