from bs4 import BeautifulSoup
import concurrent.futures
import csv
import json
import re
import requests
from datetime import datetime


webpage = requests.get('https://www.fundsexplorer.com.br/funds/atsa11').content
soup = BeautifulSoup(webpage, 'html.parser')

regex_date = re.compile(r'\"labels\"\:(\[.+\"\])')
regex_data = re.compile(r'data\"\:(\[.+\d\])')


def description():
    try:
        description_section = soup.find("section", {"id": "description"})
        description_content_wrapper = description_section.find("div", {"id": "description-content-wrapper"})
        description_content_wrapper_2 = description_content_wrapper.find("div", {"id": "description-content-description"})
        description_paragraphs = description_content_wrapper.find('p').text.split('Características do fundo')[0]
        description_paragraphs = description_paragraphs.replace("\r\n", " ").strip()
    except Exception as err:
        print(err)
    else:
        return description_paragraphs


def _basic_info_section():
    _basic_info_section = soup.find("section", {"id": "basic-infos"})
    basic_info_li = _basic_info_section.find_all('li')
    return basic_info_li

def segment():
    try:
        basic_info_li = _basic_info_section()
        segment_li = basic_info_li[-5]
        segment_tag = segment_li.text.strip()
        segment_text = " ".join(segment_tag.split()).replace('Segmento', '').strip()
    except Exception as err:
        print(err)
    else:
        return segment_text


def performance_fee():
    try:
        basic_info_li = _basic_info_section()
        basic_info_li_performance = basic_info_li[6]
        fii_performance = basic_info_li_performance.text.strip()
        fii_text_performance = " ".join(fii_performance.split()).split('performance')[1].strip()
    except Exception as err:
        print(err)
    else:
        return fii_text_performance

def administration_fee():
    try:
        basic_info_li = _basic_info_section()
        basic_info_li_administration = basic_info_li[-3]
        fii_administration = basic_info_li_administration.text.strip()
        fii_text_administration = " ".join(fii_administration.split()).split('administração')[1].strip()
    except Exception as err:
        print(err)
    else:
        return fii_text_administration

def _data_from_graphics(chart_wraper):
    graphics_div = soup.find("div", {"id": chart_wraper})
    graphics_script_tag = graphics_div.find('script')
    dates = regex_date.findall(str(graphics_script_tag), re.MULTILINE)[0].split(r',"labelColors"')[0]
    dates = dates.replace("\"", "").strip('][')
    dates = dates.split(',')
    data = regex_data.findall(str(graphics_script_tag), re.MULTILINE)[0]
    data = data.replace("\"", "").strip('][')
    data = data.split(',')
    return dates, data, graphics_script_tag, regex_data

def _transform_dates(chart_wraper):
    dates = _data_from_graphics(chart_wraper)[0]
    new_dates = []
    for date in dates:
        date = date.split('/')
        new_dates.append(date)
    numbered_dates = {
        "Janeiro": "01",
        "Fevereiro": "02",
        "Março": "03",
        "Abril": "04",
        "Maio": "05",
        "Junho": "06",
        "Julho": "07",
        "Agosto": "08",
        "Setembro": "09",
        "Outubro": "10",
        "Novembro": "11",
        "Dezembro": "12"
    }
    dates = []
    for date in new_dates:
        dates.append(date[1] + '-' + numbered_dates[date[0]])
    dates_to_be_inserted = [datetime.strptime(date, '%Y-%m') for date in dates]
    # teste = [print(datetime.strptime(date, '%Y-%m')) for date in dates]
    return dates_to_be_inserted


def dividends():
    try:
        dates = _transform_dates("dividends-chart-wrapper")
        dividends = _data_from_graphics("dividends-chart-wrapper")[1]
        dividends_list = []
        for x in range(0, len(dates)):
            dividends_list.append({'date': dates[x], 'value': dividends[x]})
    except Exception as err:
        print(err)
    else:
        return dividends_list

def dividend_yields():
    try:
        dates = _transform_dates("yields-chart-wrapper")
        dividend_yields = _data_from_graphics("yields-chart-wrapper")[1]
        dividend_yields_list = []
        for x in range(0, len(dates)):
            dividend_yields_list.append({'date': dates[x], 'value': dividend_yields[x]})
    except Exception as err:
        print(err)
    else:
        return dividend_yields_list

def patrimonial_value():
    try:
        dates = _transform_dates("patrimonial-value-chart-wrapper")
        patrimonial_value = _data_from_graphics("patrimonial-value-chart-wrapper")[1]
        patrimonial_value_list = []
        for x in range(0, len(dates)):
            patrimonial_value_list.append({'date': dates[x], 'value': patrimonial_value[x]})
    except Exception as err:
        print(err)
    else:
        return patrimonial_value_list

def vacancy():
    try:
        dates = _transform_dates("vacancy-chart-wrapper")
        graphics_script_tag = _data_from_graphics("vacancy-chart-wrapper")[2]
        regex_data = _data_from_graphics("vacancy-chart-wrapper")[3]
        vacancia_fisica = regex_data.findall(str(graphics_script_tag), re.MULTILINE)[0].split(r'"data":')[1].split(r',"backgroundColor"')[0]
        vacancia_fisica = json.loads(vacancia_fisica)
        vacancia_financeira = regex_data.findall(str(graphics_script_tag), re.MULTILINE)[0].split(r'"data":')[3]
        vacancia_financeira = json.loads(vacancia_financeira)
        vacancies_list = []
        for x in range(0, len(dates)):
            vacancies_list.append({'date': dates[x], 'physical': vacancia_fisica[x], 'financial': vacancia_financeira[x]})
    except Exception as err:
        print(err)
    else:
        return vacancies_list

def non_historical_data():
    non_historical_data = dict()
    non_historical_data['description'] = description()
    non_historical_data['segment'] = segment()
    non_historical_data['performance_fee'] = performance_fee()
    non_historical_data['administration_fee'] = administration_fee()
    return non_historical_data

def historical_data():
    historical_data = dict()
    historical_data['dividends'] = dividends()
    historical_data['dividend_yields'] = dividend_yields()
    historical_data['patrimonial_value'] = patrimonial_value()
    historical_data['vacancy'] = vacancy()
    return historical_data

print(historical_data())