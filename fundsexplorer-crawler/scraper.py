import requests
from bs4 import BeautifulSoup
import json
import csv
import concurrent.futures

# Pegando todos os fundos da primeira página
webpage = requests.get('https://www.fundsexplorer.com.br/funds').content
soup = BeautifulSoup(webpage, 'html.parser')

first_page_divs = soup.find("div", {"id": "fiis-list-container"})
first_page_a = first_page_divs.find_all('a')

nao_listadas = ['btgm11', 'eva11', 'omc11', 'mac11', 'ovl11b', 'rit11b', 'amb11b', 'aed11', 'cas11', 'exc11', 'cfl11', 'igs11', 'ci11', 'iib11', 'iip11b', 'isc11', 'ivn11', 'inf11', 'lma11', 'png11', 'mof11', 'lrp11', 'pab11', 'oft11', 'vbi11', 'vpq11', 'chb11', 'ewl11', 'ewu11', 'vho11', 'lu11', 'vif11b', 'adi11', 'aag11', 'aic11b', 'cpf11', 'il11', 'are11', 'eqr11', 'ip11', '11', 'hph11', 'hdp11b', 'hop11', 'jau11', 'ptw11', 'trx11', 'pvj11', 'bsr11', 'rpr11']
funds = []
for a in first_page_a:
    single_link = a['href'].strip('/funds/')
    if single_link not in nao_listadas:
        funds.append(single_link)



# Criando array de urls a partir dos tickers de fundos coletados
prefix = 'https://www.fundsexplorer.com.br/funds/'
urls = []
for fund in funds:
    urls.append(prefix + fund)

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

        new_dict['ticker'] = url[39:]
        new_dict['taxa de performance'] = text_perfomance
        new_dict['taxa de administração'] = text_administracao
        new_dict['Last Month Dividend Yield'] = td_dividend_yield_last_month
        new_dict['Last Year Dividend Yield'] = td_dividend_yield_last_year

        dicts.append(new_dict)
        print(url)
    except:
        webpage = requests.get(url).content
        soup = BeautifulSoup(webpage, 'html.parser')

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

        new_dict['ticker'] = url[39:]
        new_dict['taxa de performance'] = text_perfomance
        new_dict['taxa de administração'] = text_administracao
        new_dict['Last Month Dividend Yield'] = 'N/A'
        new_dict['Last Year Dividend Yield'] = 'N/A'
        dicts.append(new_dict)

        print('Only Perforandce and Adm: ' + url)



with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(getData, urls)

keys = dicts[0].keys()
with open('fundsExplorer2.csv', 'a', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(dicts)