"""
### Please note: This file is not for execution ###
"""

import requests
import json

"""
ReadJson.py
"""
response = requests.get("http://data.ntpc.gov.tw/api/v1/rest/datastore/382000000A-000352-001")
content = response.content
json_tree = json.loads(content)

for bike_rent_records in json_tree["result"]["records"]:
    leftRatio = float(bike_rent_records["sbi"]) / float(bike_rent_records["tot"]) * 100
    print("ID:{0} Left:{2:%0.1f} Name:{1}".format(bike_rent_records["sno"], bike_rent_records["aren"], leftRatio))

"""
ReadRSS.py
"""

import feedparser

# retrieve RSS feedback
content = feedparser.parse("https://www.ft.com/?edition=international&format=rss")

contentWSJ = feedparser.parse("http://www.wsj.com/public/page/rss_news_and_feeds.html")

# list all titles
print("\nTitles-------------------------\n")
for index, item in enumerate(content.entries):
    print("{0}.{1}".format(index, item["title"]))

# list all description
print("\r\nDescriptions-------------------\r\n")
for index, item in enumerate(content.entries):
    print("{0}.{1}\n".format(index, item["description"]))

"""
NasdaqNewsScraping.py
"""

import requests
from bs4 import BeautifulSoup as soup
import datetime
import pandas as pd
import os

# Using the requests module to get source code from the url
nasdaq_url = 'http://www.nasdaq.com/news/market-headlines.aspx'
url_request = requests.get(nasdaq_url)
url_content = url_request.content
# Using BeautifulSoup to parse webpage source code
parsed_content = soup(url_content)
# Finding all the <p> tag content
containers = parsed_content.find_all('p')

# initial empty list to load the data
link_list = []
title_list = []
time_list = []
tag_list = []

for container in containers:
    # Using .find_all() method to search tag name and attribute
    container_a = container.find_all('a', {"id": "two_column_main_content_la1_rptArticles_hlArticleLink_0"})
    for item in container_a:
        # Loop in the <a> tag
        news_link = item.get('href').strip()  # strip() method can remove specific chars at the head and tail
        news_title = item.text.strip()
        link_list.append(news_link)
        title_list.append(news_title)
    container_span = container.find_all('span', {'class': 'small'})
    for item in container_span:
        item_split = item.text.split(' - ')
        print(item_split)
        time = datetime.datetime.strptime(item_split[0], '%m/%d/%Y %I:%M:%S %p')
        # Formatting date see further more: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        time_list.append(time)
        # Using try...except to catch unexpected condition so that program can keep running
        try:
            tag = item_split[1].split('  in ')[1].strip()
        except Exception:
            # If the tag doesn't exist, mark it as an empty list
            tag = []
        tag_list.append(tag)
nasdaq_info = zip(title_list, time_list, link_list, tag_list)
nasdaq_info_df = pd.DataFrame(list(nasdaq_info), columns=['title', 'time', 'link', 'tag'])
nasdaq_info_df.to_csv(os.getcwd() + '/DEDA_Class_2017_WebScrapingIntro/Nasdaq_News.csv')

"""
NasdaqNewsScraping_Function.py
"""

from bs4 import BeautifulSoup as soup
import requests
import datetime
import os
import pandas as pd
import pickle


def nasdaq_news_scraping(page=1, refresh=False):
    # Argument page equals 1 by default
    if page == 1:
        # Visit the home page if page equals 1
        nasdaq_url = 'http://www.nasdaq.com/news/market-headlines.aspx'
    else:
        # Change url by different argument
        nasdaq_url = 'http://www.nasdaq.com/news/market-headlines.aspx?page=' + str(page)

    if (not os.path.exists(direct + '/temp/' + str(page) + '.pkl')) or (refresh is True):
        # connect to the website if the webpage source code file is not exist of we need to refresh it
        url_request = requests.get(nasdaq_url)
        # save the request object after scraping
        with open(direct + '/temp/' + str(page) + '.pkl', 'wb') as url_file:
            pickle.dump(url_request, url_file)
    else:
        # else, we open the source code file from local disk to save time
        with open(direct + '/temp/' + str(page) + '.pkl', 'rb') as url_file:
            url_request = pickle.load(url_file)
    url_content = url_request.content
    parsed_content = soup(url_content)
    containers = parsed_content.find_all('p')

    title_list_page = []
    time_list_page = []
    link_list_page = []
    tag_list_page = []

    for container in containers:
        container_a = container.find_all('a', {"id": "two_column_main_content_la1_rptArticles_hlArticleLink_0"})
        for item in container_a:
            news_link = item.get('href').strip()
            news_title = item.text.strip()
            title_list_page.append(news_title)
            print(news_title)
            link_list_page.append(news_link)
            print(news_link)
        container_span = container.find_all('span', {'class': 'small'})
        for item in container_span:
            item_split = item.text.split(' - ', 1)
            time = datetime.datetime.strptime(item_split[0], '%m/%d/%Y %I:%M:%S %p')
            time_list_page.append(time)
            print(time)
            try:
                tag = item_split[1].split('  in ')[1].strip()
            except Exception:
                tag = []
            tag_list_page.append(tag)
            print(tag)
    return title_list_page, time_list_page, link_list_page, tag_list_page


direct = os.getcwd() + '/DEDA_Class_2017_WebScrapingIntro'

title_list = []
time_list = []
link_list = []
tag_list = []

for page_num in range(1, 10):
    print("\nThis is Page: ", page_num)
    # Using the function defined previously with certain arguments as input
    nasdaq_news_page = nasdaq_news_scraping(page=page_num, refresh=False)
    title_list.extend(nasdaq_news_page[0])
    time_list.extend(nasdaq_news_page[1])
    link_list.extend(nasdaq_news_page[2])
    tag_list.extend(nasdaq_news_page[3])

nasdaq_info = zip(title_list, time_list, link_list, tag_list)
nasdaq_info_df = pd.DataFrame(list(nasdaq_info), columns=['title', 'time', 'link', 'tag'])
nasdaq_info_df.to_csv(direct + '/Nasdaq_News_MultiPages.csv')

"""
ChinaCities_WeatherPageScraping.py
"""

"""
This is a preliminary tutorial for scraping web pages

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
