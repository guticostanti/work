import re

url = 'https://www.fundsexplorer.com.br/funds/omc11'
regex_ticker = r'([^\/]+$)'


teste = re.search(regex_ticker, url)
teste = teste.group(0)


print(teste)