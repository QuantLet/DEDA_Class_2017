"""
This is a preliminary tutorial for scraping web pages

With a lot of notes, one can easily get touch web scraping with Python

Python Version: 3.6.2

@Author: Junjie Hu, jeremy.junjie.hu@gmail.com

"""

# Import all the packages you need, always remember that you can find 99% packages you need in python
import requests  # take the website source code back to you
import urllib  # some useful functions to deal with website URLs
from bs4 import BeautifulSoup as soup  # a package to parse website source code
import numpy as np  # all the numerical calculation related methods
import re  # regular expression package
import itertools  # a package to do iteration works
import pickle  # a package to save your file temporarily
import pandas as pd  # process structured data

save_path = 'output/'  # the path you save your files

base_link = 'http://www.tianqihoubao.com/lishi/'  # This link can represent the domain of a series of websites


def city_collection():
    request_result = requests.get(base_link)  # get source code
    parsed = soup(request_result.content)  # parse source code

    dt_items = parsed.find_all('dt')  # find the items with tag named 'dt'
    for item in dt_items:
        # iterate within all the items
        province_name = item.text.strip()  # get name of the province
        province_link2cities = item.find('a')['href']  # get link to all the cities in the province
        province = {'province_link': province_link2cities}
        provinces[province_name] = province  # save dict in the dict

    for province in provinces.keys():
        # iterate with the province link to find all the cities
        cities = {}
        print(provinces[province]['province_link'])
        request_province = requests.get(urllib.parse.urljoin(base_link, provinces[province]['province_link']))
        # use the urllib package to join relative links in the proper way
        parsed_province = soup(request_province.content)
        dd_items = parsed_province.find_all('dd')
        for dd_item in dd_items:
            print(dd_item)
            cities_items = dd_item.find_all('a')
            for city_item in cities_items:
                city_name = city_item.text.strip()
                city_link = city_item.get('href').split('.')[0]
                cities[city_name] = city_link
        provinces[province]['cities'] = cities
    return provinces


def weather_collection(link):
    """
    use the link to collect the weather data
    :param link: url link
    :return: dict, weather of a city everyday
    """
    weather_page_request = requests.get(link)
    parsed_page = soup(weather_page_request.content)
    tr_items = parsed_page.find_all('tr')
    month_weather = dict()
    for tr_item in tr_items[1:]:
        # print(tr_item)
        # daily_weather = dict()
        td_items = tr_item.find_all('td')
        date = td_items[0].text.strip()
        split_pattern = r'[\n\r\s]\s*'
        weather_states = ''.join(re.split(split_pattern, td_items[1].text.strip()))
        temperature = ''.join(re.split(split_pattern, td_items[2].text.strip()))
        wind = ''.join(re.split(split_pattern, td_items[3].text.strip()))
        month_weather[date] = {
            'weather': weather_states,
            'tempe': temperature,
            'wind': wind
        }
        # month_weather.append(daily_weather)
    return month_weather


# Nice way to get a date string with certain format
years = np.arange(start=2011, stop=2018)
months = np.arange(start=1, stop=13)
it = list(itertools.product(years, months))
date = [str(ele[0]) + format(ele[1], '02d') for ele in it]  # '02d' means 2 digits

#  ==== Since I have already download the links to all the cities, you just need to execute from here:=====
#  ==== Otherwise, use function below to retrieve provinces information ======
provinces = dict()  # initialize a dictionary to hold provinces information
# This dictionary includes 'province_link' which means links to find the cities for each province
# and the 'cities' which means city names and links
# provinces_info = city_collection()  # Use this function to retrieve links to all the cities

# This is called context management, with open can close the document automatically when the
with open('DEDA_Class_2017_WebScrapingIntro/output_cities_link.pkl', 'rb') as cities_file:  # write, change 'rb' -> 'wb'
    provinces_info = pickle.load(cities_file)
    print(provinces_info)
    # pickle.dump(provinces_info, cities_file)  # write

weather_record = dict()
# The structure is dict in dict
# first layer keyword is province name
# In each province you can find the cities
# In each city, you can find the date, in the date, you can find weather record
for key in provinces_info.keys():
    # Iterate over different provinces
    print(key)
    for city_name, city_link in provinces_info[key]['cities'].items():
        # Iterate cities within each provinces
        print(city_name)
        for month_date in date:
            # Iterate over different months
            print(city_name)
            print(month_date)
            print(provinces_info[key]['cities'][city_name])
            print("On Scraping...")
            month_weather = weather_collection(
                urllib.parse.urljoin(base_link, city_link) + '/month/' + month_date + '.html')
            weather_record[key] = {city_name: {month_date: month_weather}}
print('Finished Scraping.')

# Quiz: Try to convert the "json"-like format to pandas DataFrame
