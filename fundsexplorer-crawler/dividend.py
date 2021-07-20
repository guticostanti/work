import requests
from bs4 import BeautifulSoup
import re

webpage = requests.get('https://www.fundsexplorer.com.br/funds/abcp11').content
soup = BeautifulSoup(webpage, 'html.parser')


div_dividends_yields_chart = soup.find("div", {"id": "dividends-chart-wrapper"})
dividends_script = div_dividends_yields_chart.find('script')
regex_date = r'\"labels\"\:(\[.+\"\])'
regex_yields = r'data\"\:(\[.+\d\])'

dates = re.findall(regex_date, str(dividends_script), re.MULTILINE)[0].split(r',"labelColors"')[0]
dates = dates.replace("\"", "").strip('][')
dates = dates.split(',')

yields = re.findall(regex_yields, str(dividends_script), re.MULTILINE)[0]
yields = yields.replace("\"", "").strip('][')
yields = yields.split(',')

new_dict = dict(zip(dates, yields))

print(new_dict)
