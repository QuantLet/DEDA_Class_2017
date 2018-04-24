import requests
from bs4 import BeautifulSoup as soup
import json
import pandas as pd
import os
# from utils import ThreadWorker


# returns a list of yelp restaurant names based on search page
def yelp_get_biz_names(find_loc = 'Berlin', cflt = 'Chinese', page = 0): ##Default test args
    # Argument page equals 1 by default
    if page == 0:
        # Visit the home page if page equals 0
        yelp_url = 'https://www.yelp.com/search?find_loc=%s&cflt=%s' % (find_loc,cflt)
    else:
        # Change url by different argument
        yelp_url = 'https://www.yelp.com/search?find_loc=%s&cflt=%s&start=' % (find_loc,cflt) + str((page)*10)

    url_request = requests.get(yelp_url)
    url_content = url_request.content
    parsed_content = soup(url_content,"lxml")

    biz_content = parsed_content.find_all('a', {"class":"biz-name js-analytics-click"})
    biz_list = []

    for biz in biz_content:
        biz_href = biz.get('href')
        if 'adredir?' not in biz_href:
            biz_list.append(biz_href)
        else:
            continue
    return biz_list

# Define the function to read the first page of reviews of each biz
def yelp_get_biz_reviews(biz):
    # get single biz url
    yelp_biz_url = 'https://www.yelp.com/%s' % biz
    url_request = requests.get(yelp_biz_url)
    url_content = url_request.content
    # Using BeautifulSoup to parse webpage source code
    parsed_content = soup(url_content, "lxml")
    # Finding all the <script type="application/ld+json"> tag content
    containers = parsed_content.find('script', {"type": "application/ld+json"})
    containers_content = containers.contents[0]
    # Deserialized the content to python dictionary
    containers_content_dict = json.loads(containers_content)

    # initial empty list to load the data
    review_list = []
    # get all the reviews in the content dict
    reviews = containers_content_dict['review']
    # extract useful attributes in each review and add to review_list
    for item in reviews:
        restr_name = containers_content_dict['name']
        restr_cuis = containers_content_dict['servesCuisine']
        restr_rating = containers_content_dict['aggregateRating']['ratingValue']
        restr_price_range = containers_content_dict['priceRange']
        review_rating = item['reviewRating']['ratingValue']
        review_date = item['datePublished']
        review_desc = item['description']
        review_list.append(
            [restr_name, restr_cuis, float(restr_rating), restr_price_range,
             int(review_rating), review_date, review_desc])
    return review_list

biz_berlin_chi_20 = []

# get the biz names of the first two pages
for i in range(0, 2):
    biz_berlin_chi_20.extend(yelp_get_biz_names('Berlin', 'Chinese', i))

print(biz_berlin_chi_20)

biz_berlin_chi_20_reviews = []

for biz in biz_berlin_chi_20:
    biz_berlin_chi_20_reviews.extend(yelp_get_biz_reviews(biz))


review_info_df = pd.DataFrame(biz_berlin_chi_20_reviews, columns=['Restaurant Name', 'Cuisine', 'Rating', 'Price Range','Review Rating', 'Review Date', 'Review'])
review_info_df.to_csv(os.getcwd() + '\\Reviews_cn.csv', index=False)
