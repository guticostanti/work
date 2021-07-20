import requests
from bs4 import BeautifulSoup
import re

webpage = requests.get('https://www.fundsexplorer.com.br/funds/abcp11').content
soup = BeautifulSoup(webpage, 'html.parser')


div_yields_chart = soup.find("div", {"id": "yields-chart-wrapper"})
script = div_yields_chart.find('script')

regex_date = r'\"labels\"\:(\[.+\"\])'
regex_yields = r'data\"\:(\[.+\d\])'

dates = re.findall(regex_date, str(script), re.MULTILINE)[0].split(r',"labelColors"')[0]
dates = dates.replace("\"", "").strip('][')
dates = dates.split(',')

yields = re.findall(regex_yields, str(script), re.MULTILINE)[0]
yields = yields.replace("\"", "").strip('][')
yields = yields.split(',')

dividend_yields_dict = dict(zip(dates, yields))



print(dividend_yields_dict)
# print(labels)
# print('..................................')
# print(yields)

# DICT.KEYS E DICT.VALUES
