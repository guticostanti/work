from bs4 import BeautifulSoup
import concurrent.futures
import csv
import json
import re
import requests

### teste ###
url = 'https://www.fundsexplorer.com.br/funds/atsa11'

webpage = requests.get(url).content
soup = BeautifulSoup(webpage, 'html.parser')
### fim do teste ###



def get_tickers():
    webpage = requests.get('https://www.fundsexplorer.com.br/funds').content
    soup = BeautifulSoup(webpage, 'html.parser')
    first_page_divs = soup.find("div", {"id": "fiis-list-container"})
    first_page_a = first_page_divs.find_all('a')
    nao_listadas = ['btgm11', 'eva11', 'omc11', 'mac11', 'ovl11b', 'rit11b', 'amb11b', 'aed11', 'cas11', 'exc11', 'cfl11', 'igs11', 'ci11', 'iib11', 'iip11b', 'isc11', 'ivn11', 'inf11', 'lma11', 'png11', 'mof11', 'lrp11', 'pab11', 'oft11', 'vbi11', 'vpq11', 'chb11', 'ewl11', 'ewu11', 'vho11', 'lu11', 'vif11b', 'adi11', 'aag11', 'aic11b', 'cpf11', 'il11', 'are11', 'eqr11', 'ip11', '11', 'hph11', 'hdp11b', 'hop11', 'jau11', 'ptw11', 'trx11', 'pvj11', 'bsr11', 'rpr11']
    tickers = []
    for a in first_page_a:
        single_link = a['href'].strip('/funds/')
        if single_link not in nao_listadas:
            tickers.append(single_link)
    return tickers


def get_urls():
    tickers = get_tickers()
    prefix = 'https://www.fundsexplorer.com.br/funds/'
    urls = []
    for ticker in tickers:
        urls.append(prefix + ticker)
    return urls

def parse_url():
    ########### URL DE TESTE ###########
    url = 'https://www.fundsexplorer.com.br/funds/atsa11'
    webpage = requests.get(url).content
    soup = BeautifulSoup(webpage, 'html.parser')
    return soup

def get_description():
    description_section = soup.find("section", {"id": "description"})
    description_content_wrapper = description_section.find("div", {"id": "description-content-wrapper"})
    description_content_wrapper_2 = description_content_wrapper.find("div", {"id": "description-content-description"})
    description_paragraphs = description_content_wrapper.find('p').text.split('Características do fundo')[0]

def get_basic_info_section():
    basic_info_section = soup.find("section", {"id": "basic-infos"})
    basic_info_li = basic_info_section.find_all('li')

def get_segment():
    getBasicInfoSection()
    segment_li = basic_info_li[-5]
    segment = segment_li.text.strip()
    segment_text = " ".join(segment.split()).replace('Segmento', '').strip()

def get_performance_fee():
    getBasicInfoSection()
    basic_info_li_performance = basic_info_li[6]
    fii_performance = basic_info_li_performance.text.strip()
    fii_text_performance = " ".join(fii_performance.split()).split('performance')[1].strip()


def get_administration_fee():
    getBasicInfoSection()
    basic_info_li_administration = basic_info_li[-3]
    fii_administration = basic_info_li_administration.text.strip()
    fii_text_administration = " ".join(fii_administration.split()).split('administração')[1].strip()

def get_data_from_graphics(chart_wraper):
    graphics_div = soup.find("div", {"id": chart_wraper})
    graphics_script_tag = graphics_div.find('script')
    regex_date = r'\"labels\"\:(\[.+\"\])'
    regex_yields = r'data\"\:(\[.+\d\])'

    dates = re.findall(regex_date, str(graphics_script_tag), re.MULTILINE)[0].split(r',"labelColors"')[0]
    dates = dates.replace("\"", "").strip('][')
    dates = dates.split(',')

    yields = re.findall(regex_yields, str(graphics_script_tag), re.MULTILINE)[0]
    yields = yields.replace("\"", "").strip('][')
    yields = yields.split(',')


def get_dividends():
    div_dividend_yield_chart = soup.find("div", {"id": "dividends-chart-wrapper"})
    dividends_script = div_dividend_yield_chart.find('script')
    regex_date = r'\"labels\"\:(\[.+\"\])'
    regex_yields = r'data\"\:(\[.+\d\])'

    dates = re.findall(regex_date, str(dividends_script), re.MULTILINE)[0].split(r',"labelColors"')[0]
    dates = dates.replace("\"", "").strip('][')
    dates = dates.split(',')

    yields = re.findall(regex_yields, str(dividends_script), re.MULTILINE)[0]
    yields = yields.replace("\"", "").strip('][')
    yields = yields.split(',')

    dividends_dict = dict(zip(dates, yields))

def get_dividend_yields():
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

def patrimonio_liquido():
    div_yields_chart = soup.find("div", {"id": "patrimonial-value-chart-wrapper"})
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


def vacancy_chart_wrapper():
    div_dividend_yield_chart = soup.find("div", {"id": "vacancy-chart-wrapper"})
    dividends_script = div_dividend_yield_chart.find('script')
    regex_date = r'\"labels\"\:(\[.+\"\])'
    regex_vacancia = r'data\"\:(\[.+\d\])'


def ocupacao_fisica():
    vacancy_chart_wrapper()
    ocupacao_fisica = re.findall(regex_vacancia, str(dividends_script), re.MULTILINE)[0].split(r',"backgroundColor"')[0]


def vacancia_fisica():
    vacancy_chart_wrapper()
    vacancia_fisica = re.findall(regex_vacancia, str(dividends_script), re.MULTILINE)[0].split(r'"data":')[1].split(r',"backgroundColor"')[0]


def ocupacao_financeira():
    vacancy_chart_wrapper()
    ocupacao_financeira = re.findall(regex_vacancia, str(dividends_script), re.MULTILINE)[0].split(r'"data":')[2].split(r',"backgroundColor"')[0]


def vacancia_financeira():
    vacancy_chart_wrapper()
    vacancia_financeira = re.findall(regex_vacancia, str(dividends_script), re.MULTILINE)[0].split(r'"data":')[3]





# lista de dicionários com informações de cada fundo
dicts = []

def create_dictionary():
    new_dict = dict()
    regex_ticker = r'([^\/]+$)'
    ticker = re.search(regex_ticker, url)
    ticker = ticker.group(0)
    new_dict['ticker'] = ticker
    new_dict['taxa de performance'] = fii_text_performance
    new_dict['taxa de administração'] = fii_text_administration
    new_dict['Last Month Dividend Yield'] = td_dividend_yield_last_month
    new_dict['Last Year Dividend Yield'] = td_dividend_yield_last_year
    dicts.append(new_dict)



# with concurrent.futures.ThreadPoolExecutor() as executor:
#     executor.map(getData, urls)

# keys = dicts[0].keys()
# with open('fundsExplorer.csv', 'a', newline='')  as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(dicts)

######     TESTES      ##########


print(parse_url)




