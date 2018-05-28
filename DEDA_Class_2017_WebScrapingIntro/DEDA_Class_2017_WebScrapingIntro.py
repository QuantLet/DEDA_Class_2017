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

#list all titles
print("\nTitles-------------------------\n")
for index, item in enumerate(content.entries):
    print("{0}.{1}".format(index, item["title"]))


#list all description
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
    container_a = container.find_all('a', {"id":"two_column_main_content_la1_rptArticles_hlArticleLink_0"})
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
        container_a = container.find_all('a', {"id":"two_column_main_content_la1_rptArticles_hlArticleLink_0"})
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

for page_num in range(1,10):
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

