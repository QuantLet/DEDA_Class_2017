# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 18:45:10 2017

@author: Alex
"""
#Scrap the data from bitcoin magazin. We are first interested in the link,titel,time and the tag of the first page.


'''
functional programed
'''
from bs4 import BeautifulSoup as soup
import requests
import datetime
import os
import pandas as pd
import pickle

import bitcoinfunc as bc




title_list = []
time_list = []
link_list = []
tag_list = []
content_list = [] 



for page_num in range(1,60):
    print("\nThis is Page: ", page_num)
    # Using the function defined previously with certain input arguments
    bitcoin_news_page = bc.bitcoin_news_scraping(page=page_num, refresh=False)
    title_list.extend(bitcoin_news_page[0])
    time_list.extend(bitcoin_news_page[1])
    link_list.extend(bitcoin_news_page[2])
    tag_list.extend(bitcoin_news_page[3])
bitcoin_info = zip(title_list, time_list, link_list, tag_list)
bitcoin_info_df = pd.DataFrame(list(bitcoin_info), columns=['title', 'time','link', 'tag'])
bitcoin_info_df.to_csv(direct + '/Bitcoin_News_MultiPages.csv')


bitcoin_magazin = zip(title_list, time_list, link_list, tag_list, content_list)
bitcoin_magazin_df = pd.DataFrame(list(bitcoin_magazin), columns=['title', 'time','link', 'tag', 'content'])
bitcoin_magazin_df.to_csv('Bitcoin_magazin_news.csv')

# Getting the content of each article

for i in range(len(link_list)):
    print("\nThis is Article: ", i)
    btc_content_url = link_list[i]
    url_request = requests.get(btc_content_url)
    url_content = url_request.content

    parsed_content = soup(url_content)

    containers = parsed_content.find_all('p')
    news_text = 'Article {}:'.format(i) + "\n"
    for container in containers:
        news_text += container.text.strip()
    content_list.append(news_text)

