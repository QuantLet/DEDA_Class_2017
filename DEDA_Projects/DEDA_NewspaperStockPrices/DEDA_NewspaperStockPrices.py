
# coding: utf-8

import requests
import datetime
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from stop_words import get_stop_words
import feedparser 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd

# represents an article with its important metadata
class Article:
    author = ""
    date = ""
    title = ""
    text = ""
    link = ""
    score = 0
    
    # constructor for the class Article
    def __init__(self,aut, dat, titl, txt, lin):
        self.author = aut
        self.date = dat
        self.title = titl
        self.text = txt
        self.link = lin
    
    # removing german stop words  
    def remove_stop_words(self, lang):
        stopWords = set(stopwords.words(lang))
        words = word_tokenize(self.text)
        wordsFiltered = []
        for w in words:
            if w not in stopWords:
                wordsFiltered.append(w.lower())
        return(wordsFiltered)

# webscraping object for sueddeutsche.de 
class Sueddeutsche:
    
    # loading the search
    def load_search(self,searchterm):
        driver = webdriver.Chrome("C:\\Users\\ketzler\\Desktop\\chromedriver.exe")
        for ii in range(1,3):
            #time.sleep(5) # Test #######
            if(ii == 1):
                searchString = "http://www.sueddeutsche.de/news?search="+searchterm+                "&sort=date&dep%5B%5D=politik&dep%5B%5D=wirtschaft&dep%5B%5D=geld&typ%5B%5D=article&all%5B%5D=sys&all%5B%5D=time"
                page = requests.get(searchString)        
                soup = BeautifulSoup(page.content, 'html.parser')
                searchLinks = soup.find_all('a', class_="entrylist__link")
                result= []
                for row in searchLinks:
                    result.append(row["href"])
            else:
                driver.get(searchString)
                driver.find_element_by_xpath('//*[@title="nächste Seite"]').send_keys("\n")  #.click()
                page = driver.page_source
                soup = BeautifulSoup(page, 'html.parser')
                searchLinks = soup.find_all('a', class_="entrylist__link")
                for row in searchLinks:
                    result.append(row["href"])
                searchString = driver.current_url    
        return result

    # loading of the articles 
    def get_articles(self,links):
        result = []
        for row in links:
            page = requests.get(row)
            soup = BeautifulSoup(page.content, 'html.parser')
            body_part = soup.find(class_="body")
            header_part = soup.find(class_="header")
            text =""
            texts = body_part.find_all("p")
            for row in texts:
                text += row.get_text()
            article = Article(aut = body_part.find("span"), dat = header_part.find("time")["datetime"],                               titl = header_part.find("h2").get_text(), txt = text,                              lin = row)
            result.append(article)
        print("SZ", len(result))
        return result
    
# webscraping object for faz.net
#http://www.faz.net/suche/?offset=&cid=&index=&query=VW&offset=&allboosted=&boostedresultsize=%24boostedresultsize&from=TT.MM.JJJJ&to=09.12.2017&chkBox_2=on&chkBox_3=on&chkBox_4=on&BTyp=redaktionelleInhalte&chkBoxType_2=on&author=&username=&sort=date&resultsPerPage=20
class FAZ:
     
    # loading the search
    def load_search(self,searchword):
        now = datetime.datetime.now()
        datestring = now.strftime("%d-%m-%y")
        counter = 1
        result=[]
        while counter < 20:
            if counter == 1:
                searchString = "http://www.faz.net/suche/?offset=&cid=&index=&query="+searchword+"&offset=&allboosted=&boostedresultsize=%24boostedresultsize&from=TT.MM.JJJJ&to="+                datestring+"&chkBox_2=on&chkBox_3=on&chkBox_4=on&BTyp=redaktionelleInhalte&chkBoxType_2=on&author=&username=&sort=date&resultsPerPage=20"
            else:
                searchString = "http://www.faz.net/suche/s"+str(counter)+".html?cid=&index=&query="+searchword+                "&allboosted=&boostedresultsize=%24boostedresultsize&from=TT.MM.JJJJ&to=10-12-17&chkBox_2=on&chkBox_3=on&chkBox_4=on&BTyp=redaktionelleInhalte&chkBoxType_2=on&author=Vorname+Nachname&username=Benutzername&sort=date&resultsPerPage=20"
            page = requests.get(searchString)
            soup = BeautifulSoup(page.content, 'html.parser')
            searchLinks = soup.find_all('a', class_="TeaserHeadLink")
            for row in searchLinks:
                result.append(row["href"])
            counter += 1
        return result

    # loading of the articles
    def get_articles(self,links):
        result = []
        print(len(links))
        for row in links:
            try:
                page = requests.get(row)
            except:
                newRow = "http://www.faz.net"+row
                page = requests.get(newRow)
            try:
                soup = BeautifulSoup(page.content, 'html.parser')
                article_part= soup.find(class_ =" atc-Text")
                text =""
                texts = article_part.find_all("p")
                for row in texts:
                    text += row.get_text()
                article = Article(aut = soup.find(class_ = "quelle"), dat = soup.find(class_ = "atc-MetaTime")["datetime"],                               title = soup.find(class_ = "atc-HeadlineText").get_text(), txt = text,                              lin = row)
                result.append(article)
            except:
                pass
        print("FAZ ", len(result))
        return result



class stockPriceLoader:
    
    # Upload fo sock prices from a csv file
    def getStockPrice(self):
        # loading the stock prices for a company
        data = pd.read_csv("SIE.DE.csv", sep = ",")
        data.columns = ["Date_", "Open_", "High", "Low", "Close", "Adj Close", "Volume"]
        result = pd.DataFrame(columns = ["Date_", "Price difference"])
        # compute the pricedifference
        result["Price difference"] = data["Open_"] - data["Close"]
        result["Date_"] = data["Date_"]
        return(result)

# Analyse
class Analyse:

    #create a dataFrame with two column (Date, price difference)
    def analyseArticles(self,listArticles, stockpriceDifferences):
        helper = []
        for article in listArticles: 
            ii= 0
            score = 0
            # price differenz
            row = stockpriceDifferences[stockpriceDifferences["Date_"] == article.date[0:10]]
            if row.empty:
                continue
            while ii <len(article.text):
                helper.append([article.text[ii], row.iloc[0]['Price difference']])
                ii +=1
        mlFrame = pd.DataFrame(helper, columns=["Word", "Effect"])
        return(mlFrame)                
            

####### Main ############
# Which company do we want to search?
searchterm = "Siemens"
# webscrapping sueddeutsche.de
sued = Sueddeutsche()
links = sued.load_search(searchterm)  
articleList = sued.get_articles(links)  

# webscrapping faz.net
faz = FAZ()
links2 = faz.load_search(searchterm)
articleList += faz.get_articles(links2)  

# removing stop words
for row in articleList:
    row.text = row.remove_stop_words("german")
    
##stockPriceLoader
spl = stockPriceLoader()
stockpriceDifferences = spl.getStockPrice()

#convert date format
import time
stockpriceDifferences["Date_"] = pd.to_datetime(stockpriceDifferences.Date_).dt.strftime('%Y-%m-%d')

## Analyse, returns a dataFrame with date and price difference
senti = Analyse()
mlFrame = senti.analyseArticles(articleList, stockpriceDifferences)

# 1 = rising stock prices
# 0 = failing stock prices
mlFrame["Effect"].loc[mlFrame["Effect"] > 0] = 1
mlFrame["Effect"].loc[mlFrame["Effect"] < 0] = 0

############## ML #############

## Dec. Tree
from sklearn import tree
from sklearn import preprocessing
import numpy as np

# factorize
le = preprocessing.LabelEncoder()
X = mlFrame["Word"].tolist() 
le.fit(X)
X = le.transform(X) 
#in 2d list
X = np.reshape(X, (len(X), 1))
Y = mlFrame["Effect"].tolist()
Y = np.reshape(Y, (len(Y), 1))

#train decision tree
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
#predict
print(le.inverse_transform([2]))
pred = clf.predict([[2]])
print(pred)


## Log Regression
from sklearn.linear_model import LogisticRegression

# factorize
le = preprocessing.LabelEncoder()
X = mlFrame["Word"].tolist() 
le.fit(X)
X = le.transform(X) 
#in 2d list
X = np.reshape(X, (len(X), 1))
Y = mlFrame["Effect"].tolist()
Y = np.reshape(Y, (len(Y), 1))

#train Logistic Regression
lrm = LogisticRegression()
lrm.fit(X, Y)

#predict
print(le.inverse_transform([2245]))
pred = lrm.predict([[2245]])
print(pred)

