from bs4 import BeautifulSoup as soup
import requests
import datetime
import os
import pandas as pd
import pickle
# Using the requests module to get source code from the url
direct = os.getcwd()

def bitcoin_news_scraping(page=1, refresh=False):
    # Argument page equals 1 by default
    if page == 1:
        # Visit the home page if page equals 1
        nasdaq_url = 'http://www.nasdaq.com/author/bitcoin-magazine'
    else:
        # Change url by different argument
        nasdaq_url = 'http://www.nasdaq.com/author/bitcoin-magazine?page=' + str(page)
    if (not os.path.exists(direct + '\\temp\\' + str(page) + '.pkl')) or (refresh is True):
        # connect to the website if the webpage source code file is not exist of we need to refresh it
        url_request = requests.get(nasdaq_url)
        # save the request object after scraping
        with open(direct + '\\temp\\' + str(page) + '.pkl', 'wb') as url_file:
            pickle.dump(url_request, url_file)
    else:
        # else, we open the source code file from local disk to save time
        with open(direct + '\\temp\\' + str(page) + '.pkl', 'rb') as url_file:
            url_request = pickle.load(url_file)

    url_request = requests.get(nasdaq_url)
    url_content = url_request.content
    # Using BeautifulSoup to parse webpage source code
    parsed_content = soup(url_content)
    # Finding all the <li> tag content
    containers = parsed_content.find_all('li')

    # initial empty list to load the data
    link_list = []
    title_list = []
    time_list = []
    tag_list = []

    for i in range(0, 20):
        for container in containers:
            # Using .find_all() method to search tag name and attribute
            ident_a = "main_content_rptArticles_hlArticleLink_{}".format(i)
            ident_b = "main_content_rptArticles_lbArticleInfo_{}".format(i)
            ident_c = "main_content_rptArticles_lbCategories_{}".format(i)
            container_a = container.find_all('a', {"id": ident_a})  # For more than only 0(1)!
            container_b = container.find_all('span', {"id": ident_b})
            container_c = container.find_all('span', {"id": ident_c})

            for item in container_a:
                # Loop in the <a> tag
                news_link = item.get('href').strip()
                # strip() method can remove specific chars at the head and tail
                news_title = item.text.strip()
                link_list.append(news_link)
                title_list.append(news_title)

            for item in container_b:
                news_time = datetime.datetime.strptime(item.text.strip(), '%m/%d/%Y, %I:%M %p')
                time_list.append(news_time)
            for item in container_c:
                news_tag = item.text.strip("Appears In:")
                tag_list.append(news_tag)
    return title_list, time_list,link_list, tag_list