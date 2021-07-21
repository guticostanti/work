from bs4 import BeautifulSoup
import concurrent.futures
import csv
import json
import re
import requests

def tickers():
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


def urls():
    tickers = tickers()
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

    regex_ticker = r'([^\/]+$)'
    current_ticker = re.search(regex_ticker, url)
    current_ticker = current_ticker.group(0)

    return soup, current_ticker

soup = parse_url()[0]

def description():
    description_section = soup.find("section", {"id": "description"})
    description_content_wrapper = description_section.find("div", {"id": "description-content-wrapper"})
    description_content_wrapper_2 = description_content_wrapper.find("div", {"id": "description-content-description"})
    description_paragraphs = description_content_wrapper.find('p').text.split('Características do fundo')[0]
    description_paragraphs = description_paragraphs.replace("\r\n", " ").strip()
    return description_paragraphs

def basic_info_section():
    basic_info_section = soup.find("section", {"id": "basic-infos"})
    basic_info_li = basic_info_section.find_all('li')
    return basic_info_li

def segment():
    basic_info_li = basic_info_section()
    segment_li = basic_info_li[-5]
    segment_tag = segment_li.text.strip()
    segment_text = " ".join(segment_tag.split()).replace('Segmento', '').strip()
    return segment_text


def performance_fee():
    basic_info_li = basic_info_section()
    basic_info_li_performance = basic_info_li[6]
    fii_performance = basic_info_li_performance.text.strip()
    fii_text_performance = " ".join(fii_performance.split()).split('performance')[1].strip()
    return fii_text_performance

def administration_fee():
    basic_info_li = basic_info_section()
    basic_info_li_administration = basic_info_li[-3]
    fii_administration = basic_info_li_administration.text.strip()
    fii_text_administration = " ".join(fii_administration.split()).split('administração')[1].strip()
    return fii_text_administration

def data_from_graphics(chart_wraper):
    graphics_div = soup.find("div", {"id": chart_wraper})
    graphics_script_tag = graphics_div.find('script')
    regex_date = r'\"labels\"\:(\[.+\"\])'
    regex_data = r'data\"\:(\[.+\d\])'

    dates = re.findall(regex_date, str(graphics_script_tag), re.MULTILINE)[0].split(r',"labelColors"')[0]
    dates = dates.replace("\"", "").strip('][')
    dates = dates.split(',')

    data = re.findall(regex_data, str(graphics_script_tag), re.MULTILINE)[0]
    data = data.replace("\"", "").strip('][')
    data = data.split(',')

    return dates, data, graphics_script_tag, regex_data


def dividends():
    dates = data_from_graphics("dividends-chart-wrapper")[0]
    dividends = data_from_graphics("dividends-chart-wrapper")[1]
    dividends_dict = dict(zip(dates, dividends))
    return dividends_dict

def dividend_yields():
    dates = data_from_graphics("yields-chart-wrapper")[0]
    dividend_yields = data_from_graphics("yields-chart-wrapper")[1]
    dividend_yields_dict = dict(zip(dates, dividend_yields))
    return dividend_yields_dict

def patrimonial_value():
    dates = data_from_graphics("patrimonial-value-chart-wrapper")[0]
    patrimonial_value = data_from_graphics("patrimonial-value-chart-wrapper")[1]
    patrimonial_value_dict = dict(zip(dates, patrimonial_value))
    return patrimonial_value_dict

def vacancy():
    dates = data_from_graphics("vacancy-chart-wrapper")[0]
    graphics_script_tag = data_from_graphics("vacancy-chart-wrapper")[2]
    regex_data = data_from_graphics("vacancy-chart-wrapper")[3]
    vacancia_fisica = re.findall(regex_data, str(graphics_script_tag), re.MULTILINE)[0].split(r'"data":')[1].split(r',"backgroundColor"')[0]
    vacancia_fisica = json.loads(vacancia_fisica)
    vacancia_financeira = re.findall(regex_data, str(graphics_script_tag), re.MULTILINE)[0].split(r'"data":')[3]
    vacancia_financeira = json.loads(vacancia_financeira)

    vacancies_dict = dict()
    for x in range(0, len(dates)):
        vacancies_list = {
            dates[x]: {
                "vacância física": vacancia_fisica[x],
                "vacância financeira": vacancia_financeira[x]
            }
        }
        vacancies_dict.update(vacancies_list)

    return vacancies_dict

def non_historical_data():
    current_ticker = parse_url()[1]
    non_historical_data = dict()
    non_historical_data[current_ticker] = {}
    non_historical_data[current_ticker]['Description'] = description()
    non_historical_data[current_ticker]['Segment'] = segment()
    non_historical_data[current_ticker]['Performance Fee'] = performance_fee()
    non_historical_data[current_ticker]['Administration Fee'] = administration_fee()
    return non_historical_data

def historical_data():
    current_ticker = parse_url()[1]
    historical_data = dict()
    historical_data[current_ticker] = {}
    historical_data[current_ticker]['Dividends'] = dividends()
    historical_data[current_ticker]['Dividend Yields'] = dividend_yields()
    historical_data[current_ticker]['Patrimonial Value'] = patrimonial_value()
    historical_data[current_ticker]['Vacancy'] = vacancy()
    return historical_data

print(non_historical_data())

# lista de dicionários com informações de cada fundo
# dicts = []

# def create_dictionary():
#     new_dict = dict()
#     regex_ticker = r'([^\/]+$)'
#     ticker = re.search(regex_ticker, url)
#     ticker = ticker.group(0)
#     new_dict['ticker'] = ticker
#     new_dict['taxa de performance'] = fii_text_performance
#     new_dict['taxa de administração'] = fii_text_administration
#     new_dict['Last Month Dividend Yield'] = td_dividend_yield_last_month
#     new_dict['Last Year Dividend Yield'] = td_dividend_yield_last_year
#     dicts.append(new_dict)



# with concurrent.futures.ThreadPoolExecutor() as executor:
#     executor.map(getData, urls)

# keys = dicts[0].keys()
# with open('fundsExplorer.csv', 'a', newline='')  as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(dicts)

######     TESTES      ##########

