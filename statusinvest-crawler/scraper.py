from bs4 import BeautifulSoup
import json
import psycopg2
import requests
from typing import List
import re

# def _convert_tuple_in_string(tup: tuple) -> str:
#     str = ''
#     for item in tup:
#         str = str + item
#     return str

# def tickers_from_db() -> List[str]:
#     conn = psycopg2.connect(
#         host="env6.lionx.ai",
#         database="lionx",
#         user="lionx",
#         password="FAJvJ4eCVQNexTRL")

#     cur = conn.cursor()
#     cur.execute("select distinct pk_value from equities;")
#     raw_tickers = cur.fetchall()
#     return raw_tickers

# def tickers_list() -> List[str]:
#     raw_tickers = tickers_from_db()
#     tickers = []
#     for ticker in raw_tickers:
#         ticker = _convert_tuple_in_string(ticker).lower()
#         tickers.append(ticker)
#     return tickers

# def build_stock_tickers_urls() -> List[str]:
#     tickers = tickers_list()
#     prefix = 'https://statusinvest.com.br/acoes/'
#     urls = []
#     for ticker in tickers:
#         urls.append(prefix + ticker)
#     return urls


# dicts = []

######################## TESTE ############################



# url ='https://statusinvest.com.br/acoes/petr4'
# webpage = requests.get(url).content
# soup = BeautifulSoup(webpage, 'html.parser')

def dividend_yield():
    div_dividend_yield = soup.find("div", {"title": "Dividend Yield com base nos últimos 12 meses"})
    dividend_yield_element = div_dividend_yield.find("strong", {"class": "value"}).text
    dividend_yield = dividend_yield_element + '%'
    return dividend_yield

# P/L
def preco_por_lucro():
    div_preco_por_lucro = soup.find("div", {"title": "Dá uma ideia do quanto o mercado está disposto a pagar pelos lucros da empresa."})
    preco_por_lucro = div_preco_por_lucro.find("strong", {"class": "value d-block lh-4 fs-4 fw-700"}).text
    return preco_por_lucro

# ROE
def return_on_equity():
    div_return_on_equity = soup.find("div", {"title": "Mede a capacidade de agregar valor de uma empresa a partir de seus próprios recursos e do dinheiro de investidores."})
    return_on_equity = div_return_on_equity.find("strong", {"class": "value d-block lh-4 fs-4 fw-700"}).text
    return return_on_equity

# ROA
def return_on_assets():
    div_return_on_assets = soup.find("div", {"title": "O retorno sobre os ativos ou Return on Assets, é um indicador de rentabilidade, que calcula a capacidade de uma empresa gerar lucro a partir dos seus ativos, além de indiretamente, indicar a eficiência dos seus gestores."})
    return_on_assets = div_return_on_assets.find("strong", {"class": "value d-block lh-4 fs-4 fw-700"}).text
    return return_on_assets

# Margem Líquida
def net_margin():
    div_net_margin = soup.find("div", {"title": "Revela a porcentagem de lucro em relação às receitas de uma empresa."})
    net_margin =div_net_margin.find('strong', {"class": "value d-block lh-4 fs-4 fw-700"}).text
    return net_margin



url_endpoint = 'https://statusinvest.com.br/acao/getdre?companyName=petrobras&type=1'
webpage = requests.get(url_endpoint).content
soup = BeautifulSoup(webpage, 'html.parser')

# regex_lucro_liquido = re.compile(r'\"lucroLiquido\"\:(\[.*\])')


# dict_lucro_liquido = regex_lucro_liquido.findall(str(soup), re.MULTILINE)[0][1:-1].split('},')[0] + '}'

data = json.loads(str(soup))












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

