'''
Name:   DEDA LinkedIn Scraper
Author: Paul Jakob
Date:   29.01.2018
Description:    
    This project demonstrates webscraping on the example of LinkedIn.
    The goal is to present an overview of the german Blockchain talents and present insights,
    which are not given by using a standard LinkedIn search.

'''

# importing packages for request handling, data retrieval, processing and visualization
import requests
import os
from bs4 import BeautifulSoup
import pandas
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# packages for maps visualization
import googlemaps
import gmaps
import gmplot

# packages for the gender predictions
import nltk
from nltk.corpus import names as corp
import random

# import config file with credentials - path needs to be adapted
path = "/Users/pauljakob/Docs/00_Uni/04_DEDA/Projects/DEDA_CLASS_2017_PJ"
os.chdir(path)
from CONFIG import *

# put into routine with searchterm as input parameter
# implement more secure (proofs)

'''
1. Section:
    Using the requests package to crawl over all results for a LinkedIn search
    Beatifulsoup is used to identify and extract information
'''
with requests.Session() as session:

    # set url for initial request and call website to create and retrieve session values
    url = 'https://www.linkedin.com/'
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # get all input values / loop over the inputs / identify the csrftoken and get the value
    inputs = soup.find_all('input')
    for element in inputs:
        try:
            if element['name'] == 'loginCsrfParam':
                csrfparamvalue = element['value']
        except LookupError:
            print('Lookuperror')
    # set values for the login form
    loginurl = 'https://www.linkedin.com/uas/login-submit'
    username = payload['username']
    password = payload['password']
    jsenabled = "false"

    # open up the session by logging in successfully
    login_data = dict(session_key=username,session_password=password,isJsEnabled=jsenabled,loginCsrfParam=csrfparamvalue)
    session.post(loginurl,data=login_data,headers={"referer":"https://www.linkedin.com/"})

    # Setup search parameters region and search term
    searchTerm = "blockchain"
    searchRegion = "de"
    searchString = "https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22" + searchRegion + "%3A0%22%5D&keywords=" + searchTerm + "&origin=FACETED_SEARCH"
    # Set range for the loop - should be dynamic
    amount = list(range(1,20))
    
    # Get results page for every page and store them in an array
    results = list()
    for pageNumber in amount:
        # paging string
        pagingString = "&page=" + str(pageNumber)
        searchURL = searchString + pagingString
        print(searchURL)
        page = session.get(searchURL)
        results.append(page)
    
    # empty array where all result strings are stored
    all_cities = list()
    results_per_page = list(range(1,11))
    # loop over every result page and retrieve the location
    for pages in results:
        page_soup = BeautifulSoup(pages.content, 'html.parser')
        code = page_soup.body.find_all('code')
        # the 14th code tag of each page contains the user information
        data_code = code[14].contents[0]
        # split the data string for every location 
        location_texts = data_code.split('"location":"')
        cities = list()
        # loop over locations and print out 
        for text in location_texts:
            location = text.partition(",")[0]
            print(location)
            cities.append(location)
        cities.pop(0)
        all_cities.extend(cities)
    
    # empty array where all names are stored
    all_names = list()
    # loop over every result page and retrieve the first name
    for pages in results:
        page_soup = BeautifulSoup(pages.content, 'html.parser')
        code = page_soup.body.find_all('code')
        # the 14th code tag of each page contains the user information
        data_code = code[14].contents[0]
        # split the data string for every location 
        name_texts = data_code.split('firstName":"')
        names = list()
        # loop over locations and print out 
        for text in name_texts:
            name = text.partition(",")[0]
            print(name)
            names.append(name)
        names.pop(0)
        all_names.extend(names)
    
    all_names = list(filter(lambda a: a != '"', all_names))
    all_names = list(filter(lambda a: a != 'Blockchain', all_names))
    
'''
2. Section:
    In this part of the code, the data extracted from the search results is processed.
    An overview of all available talents per city is presented in different ways.
        a) Distribution is shown in a bar chart
        b) Distribution is shown on a map by using the Google Maps API. (Markers & Heatmap)
'''    
# remove unnecessary information
length = len(all_cities)
for x in range(0, length):
    all_cities[x] = all_cities[x].replace(' und Umgebung', '')
    all_cities[x] = all_cities[x].replace('Kreisfreie Stadt ', '')

# get the count of each City and show a diagram for the location distribution
loc_count = Counter(all_cities)
loc_dataframe = pandas.DataFrame.from_dict(loc_count, orient='index').reset_index()
loc_dataframe.columns = ['Cities', 'Talents']
# sort descending
loc_dataframe = loc_dataframe.sort_values('Talents', ascending= False)

# plot the graph
y_pos = np.arange(len(loc_dataframe))

plt.bar(y_pos, loc_dataframe['Talents'], alpha=0.5)
plt.xticks(y_pos, loc_dataframe['Cities'])
plt.ylabel('Talents')
plt.title('Blockchain Talents per city in Germany')
plt.xticks(rotation=90)
plt.savefig('Cities0.png')
plt.show()

# Maps integration 
api_key = payload['api_key']
gmaps = googlemaps.Client(key=api_key)

# Geocoding a city
# geocode_result = gmaps.geocode(all_cities[0])

latitudes = list()
longitudes = list()

# loop over all cities and get the geocoding --> also for duplicates for density on heatmap
for city in all_cities:
    try:
        geocode_result = gmaps.geocode(city)
        
        lngDif = (geocode_result[0]['geometry']['bounds']['southwest']['lng'] - geocode_result[0]['geometry']['bounds']['northeast']['lng'])/ 2
        latDif = (geocode_result[0]['geometry']['bounds']['southwest']['lat'] - geocode_result[0]['geometry']['bounds']['northeast']['lat']) / 2
        
        lat = geocode_result[0]['geometry']['bounds']['northeast']['lat'] + latDif
        lng = geocode_result[0]['geometry']['bounds']['northeast']['lng'] + lngDif
        
        latitudes.append(lat)
        longitudes.append(lng)
        
    except:
        try:
            geocode_result = gmaps.geocode(city)
            geocode_result[0]['geometry']['location']['lat']
            geocode_result[0]['geometry']['location']['lng']
        except:
            print('Geocode Error')


# initialize the map
gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 16)            

# try different plots / heatmap, scatter, marker
gmap.heatmap(latitudes, longitudes)
#gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
#gmap.scatter(latitudes, longitudes, '#3B0B39', size=40, marker=False)
gmap.scatter(latitudes, longitudes, 'k', marker=True)

gmap.draw("TalentMapAll.html")

'''
3. Section:
    The following part deals with the identification of genders by applying machine learning techniques.
    A neural network is trained by using census data available via: https://www.ssa.gov/oact/babynames/limits.html
    It then is used to categorize all people that have been found by gender.
'''

# helper function
def gender_features(name):
    return {"last_letter": name[-1],
            "vowel": (name[-1] in 'aeiouy')}  # feature set

# remove unnecessary information of the first names (double name, titles, etc)
length_n = len(all_names)
idx_pop = list()
for x in range(0, length_n):
    if len(all_names[x]) < 2:
        # remove entries that aren't names
        idx_pop.append(x)
    else:
        # check for and remove all possible disruptions in strings
        all_names[x] = all_names[x].replace('Dr. ', '') # title
        all_names[x] = all_names[x].replace('"', '') # end character
        all_names[x] = all_names[x].split(' ', 1)[0] # two first names
        all_names[x] = all_names[x].split('-', 1)[0] # double names
# only one to pop therefore no loop
all_names.pop(idx_pop[0])

# Now the model prediction starts - Using NLKTs Naive Bayes Model
# retrieve test set
labeled_names = ([(name, "male") for name in corp.words("male.txt")] +
                     [(name, "female") for name in corp.words("female.txt")])

# Mix up the list
random.shuffle(labeled_names)

#Process the names through feature extractor
feature_sets = [(gender_features(n), gender)
                for (n, gender) in labeled_names]

# Divide the feature sets into training and test sets
train_set, test_set = feature_sets[500:], feature_sets[:500]

# Train the naiveBayes classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

# Test the accuracy of the classifier on the test data
print(nltk.classify.accuracy(classifier, test_set))  # returns 81%

# Predict the gender for all names in the list
all_genders = list()
length_g = len(all_names)
for x in range(0, length_g):
    gender = classifier.classify(gender_features(all_names[x]))
    print(gender)
    all_genders.append(gender)

gender_count = Counter(all_genders)
gender_dataframe = pandas.DataFrame.from_dict(gender_count, orient='index').reset_index()
gender_dataframe.columns = ['Gender', 'Talents']
# sort descending
gender_dataframe = gender_dataframe.sort_values('Talents', ascending= False)

# plot the graph
y_pos_g = np.arange(len(gender_dataframe))

plt.bar(y_pos_g, gender_dataframe['Talents'])
plt.xticks(y_pos_g, gender_dataframe['Gender'])
plt.ylabel('Talents')
plt.title('Gender distribution for BC Talents in Germany')
plt.xticks(rotation=90)

plt.show()
plt.savefig('Gender.png')
plt.savefig('demo.png', transparent=True)

'''
Possible Improvements:
    1. Modularization into class or methods
    2. loop over results could be combined
'''