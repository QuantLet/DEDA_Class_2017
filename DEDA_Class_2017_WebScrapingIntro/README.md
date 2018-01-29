
[<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/banner.png" width="888" alt="Visit QuantNet">](http://quantlet.de/)

## [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/qloqo.png" alt="Visit QuantNet">](http://quantlet.de/) **Digital Economy and Decision Analytics** [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/QN2.png" width="60" alt="Visit QuantNet 2.0">](http://quantlet.de/)

```yaml

Name of Quantlet : DEDA_Class_2017_WebScrapingIntro
Published in : Digital Economy and Decision Analytics
Description : 
- Demonstrate getting data from webpage API and scraping news information from nasdaq.com
- Introducing functional programming and object-oriented programming
Keywords :
- Python
- Teaching
- Web Data
- RSS
- Json
- HTML
- BeautifulSoup
- OOP
Author : Junjie Hu, Cathy YH Chen, Roméo Després 

```

### Python Code:
```python

"""
### Please note: This file is not for execution ###
"""

import requests
import json

"""
ReadJson.py
"""
import requests
import json
import pprint

response = requests.get("http://data.ntpc.gov.tw/api/v1/rest/datastore/382000000A-000352-001")
content = response.content
json_tree = json.loads(content)
pprint.pprint(json_tree)

for bike_rent_records in json_tree["result"]["records"]:
    leftRatio = float(bike_rent_records["sbi"]) / float(bike_rent_records["tot"]) * 100
    print("ID:{0} Left:{2:0.1f}% Name:{1}".format(bike_rent_records["sno"], bike_rent_records["aren"], leftRatio))


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
ReadCRIX.py
"""

import requests
import json
import pandas as pd

url = 'http://crix.hu-berlin.de/data/crix.json'
r = requests.get(url)

content = r.content

js_content = json.loads(content)
for item in js_content:
    print(item)

data_raw = pd.DataFrame(js_content)
data_raw.set_index(keys='date', inplace=True)

data_raw.plot()


"""
ReadXML.py
"""

import requests
import xml.dom.minidom

response = requests.get(
    "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Datasets/daily_treas_bill_rates.xml")
content = response.content
dataDOM = xml.dom.minidom.parseString(content)
response = requests.get(
    "https://news.google.com/news/rss/headlines/section/q/finance%20news/finance%20news?ned=us&hl=en")



"""
NasdaqNewsScraping.py
"""

import requests
from bs4 import BeautifulSoup as soup
import datetime
import pandas as pd
import os
import pickle

# Using the requests module to get source code from the url
nasdaq_url = 'http://www.nasdaq.com/news/market-headlines.aspx'

direct = os.getcwd()
# direct = os.getcwd() + '/DEDA_Class_2017_WebScrapingIntro'
refresh = False

if (not os.path.exists(direct + '/temp/' + '0.pkl')) or (refresh is True):
    # connect to the website if the webpage source code file is not exist of we need to refresh it
    url_request = requests.get(nasdaq_url)
    # save the request object after scraping
    with open(direct + '/temp/' + '0.pkl', 'wb') as url_file:
        pickle.dump(url_request, url_file)
else:
    # else, we open the source code file from local disk to save time
    with open(direct + '/temp/' + '0.pkl', 'rb') as url_file:
        url_request = pickle.load(url_file)

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


direct = os.getcwd()
# direct = os.getcwd() + '/DEDA_Class_2017_WebScrapingIntro'

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
print(os.getcwd())
nasdaq_info_df.to_csv(direct + '/Nasdaq_News_MultiPages.csv')


"""
SimpleClass_Student.py
"""

# Simple class


class Person(object):
    # The class Person is inherited from class object
    def __init__(self, first, last, gender, age):
        # self is the default argument that points to the instance
        # Using __init__ to initialize a class to take arguments
        self.first_name = first
        self.last_name = last
        self.gender = gender
        self.age = age


class Student(Person):
    # The class Student inherited from class Person
    def __init__(self, first, last, gender, age, school):
        # super() method allows us to handle the arguments from parent class without copying
        super().__init__(first, last, gender, age)
        # Child class can also be added new arguments
        self.school = school

    def describe(self):
        # describe is a method of class Student
        print('{0} {1} is a {2} years old {3} who studies at {4}.'.format(
            self.first_name,
            self.last_name,
            self.age,
            self.gender,
            self.school))


# stu_1 is an instance of class Student
stu_1 = Student('Jon', 'Doe', 'male', 10, 'C_School')
print("Is Student a subclass of Person: ", issubclass(Student, Person))
print("Is stu_1 an instance of Student: ", isinstance(stu_1, Student))
# Using the attributes in the object stu_1
print(stu_1.school)
# Using the methods in the object stu_1
print(stu_1.describe())


"""
ReadRSSClass.py
"""

import feedparser

class ReadRSS(object):
    # There are some methods with name surrounded by double underscore called "magic method"
    # Further more see: https://www.python-course.eu/python3_magic_methods.php
    def __init__(self, url):
        self.url = url
        self.response = feedparser.parse(self.url)

    def __eq__(self, other):
        # __eq__() is a magic method that enables comparison two object with ==
        if self.url == other.url:
            return True
        else:
            return False

    def __repr__(self):
        # __repr__() is a magic method that enables customization default printed format
        return "The website url is: " + self.url

    def get_titles(self):
        titles = []
        for item in self.response["entries"]:
            titles.append(item["title"])
        print("\nTITLES:\n")
        print('\n'.join(titles))
        return titles

    def get_description(self):
        scripts = []
        for item in self.response["entries"]:
            scripts.append(item["description"])
        print("\nDESCRIPTIONS:\n")
        print('\n'.join(scripts))
        return scripts


"""
ReadRSS_External.py
"""

import os
import sys

sys.path.append(os.getcwd() + '/DEDA_Class_2017_WebScrapingIntro/')
# add the module path to Python searching path
import ReadRSSClass as rrc

# ReadRSSClass is the file name of the module code


r = rrc.ReadRSS("http://www.wsj.com/xml/rss/3_7085.xml")
r2 = rrc.ReadRSS("http://www.wsj.com/xml/rss/3_7085.xml")

# Here we can print out the object's url in certain format
print(r)

# Here we use == to validate if two responses of two url are equal
if r == r2:
    print("Two urls are the same")
else:
    print("Two urls are not the same")
# Print out the titles
r.get_titles()
# Print out the descriptions
r.get_description()


"""
StockTwitsAPI.py
"""

import requests

class StockTwitsApi:

  def __init__(self):
    self.base = "https://api.stocktwits.com/api/2/"
    self.token = ""

  def login(self, token):
    self.token = token
    return(self)

  def search(self, mode=None, **kwargs):

    """ mode can have value None, "users" or "symbols"."""

    url = self.base + "search{}.json".format("" if mode is None else "/" + mode)
    if self.token != "":
      kwargs.update({"access_token": self.token})
    result = requests.get(url, params=kwargs)
    return(result)

  def stream_symbol(self, id, **kwargs):
    url = self.base + "streams/symbol/{}.json".format(id)
    if self.token != "":
      kwargs.update({"access_token": self.token})
    result = requests.get(url, params=kwargs)
    return(result)



```



