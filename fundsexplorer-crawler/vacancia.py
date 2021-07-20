import requests
from bs4 import BeautifulSoup
import re

webpage = requests.get('https://www.fundsexplorer.com.br/funds/abcp11').content
soup = BeautifulSoup(webpage, 'html.parser')


div_dividends_yields_chart = soup.find("div", {"id": "vacancy-chart-wrapper"})
dividends_script = div_dividends_yields_chart.find('script')
regex_date = r'\"labels\"\:(\[.+\"\])'
regex_vacancia = r'data\"\:(\[.+\d\])'


# dates = re.findall(regex_date, str(dividends_script), re.MULTILINE)[0].split(r',"labelColors"')[0]
# dates = dates.replace("\"", "").strip('][')
# dates = dates.split(',')

# ocupacao_fisica = re.findall(regex_vacancia, str(dividends_script), re.MULTILINE)[0].split(r'"data":')[0]
ocupacao_fisica = re.findall(regex_vacancia, str(dividends_script), re.MULTILINE)[0].split(r',"backgroundColor"')[0]

vacancia_fisica = re.findall(regex_vacancia, str(dividends_script), re.MULTILINE)[0].split(r'"data":')[1].split(r',"backgroundColor"')[0]

ocupacao_financeira = re.findall(regex_vacancia, str(dividends_script), re.MULTILINE)[0].split(r'"data":')[2].split(r',"backgroundColor"')[0]

vacancia_financeira = re.findall(regex_vacancia, str(dividends_script), re.MULTILINE)[0].split(r'"data":')[3]

# yields = yields.replace("\"", "").strip('][')
# yields = yields.split(',')

# new_dict = dict(zip(dates, yields))

# print(new_dict)

### testes ###
# print(vacancia_fisica)

print(vacancia_financeira)
