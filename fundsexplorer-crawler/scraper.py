import requests
from bs4 import BeautifulSoup
import json

webpage = requests.get('https://www.fundsexplorer.com.br/funds/wtsp11b').content

soup = BeautifulSoup(webpage, 'html.parser')

# fii - Dividend Yield
fii_section = soup.find("section", {"id": "dividends"})
fii_table = fii_section.find('table')
fii_tr = fii_table.find_all('tr')[-1]
fii_td = fii_tr.find_all('td')
td_dividend_yield_last_year = fii_td[-2].text
td_dividend_yield_last_month = fii_td[1].text

new_dict = dict()
new_dict['Last Month Dividend Yield'] = td_dividend_yield_last_month
new_dict['Last Year Dividend Yield'] = td_dividend_yield_last_year


# ETF - Taxas de Administração e Performance
etf_section = soup.find("section", {"id": "basic-infos"})
etf_li = etf_section.find_all('li')

# Taxa de performance
etf_li_performance = etf_li[6]
etf_performance = etf_li_performance.text.strip()
text_perfomance = " ".join(etf_performance.split()).split('performance')[1].strip()
performance_json_acceptable_string = '{' + "\"taxa de performance\": " + "\"" + text_perfomance + "\"" + '}'
perfomance_dict = json.loads(performance_json_acceptable_string)


# new_dict = dict()

# Taxa de adm
etf_li_administracao = etf_li[-3]
etf_administracao = etf_li_administracao.text.strip()
text_administracao = " ".join(etf_administracao.split()).split('performance')[0].strip()
administracao_json_acceptable_string = '{' + "\"taxa de administração\": " + "\"" + text_administracao + "\"" + '}'
administracao_dict = json.loads(administracao_json_acceptable_string)
