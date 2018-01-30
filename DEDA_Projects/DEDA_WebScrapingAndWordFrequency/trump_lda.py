# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 17:22:23 2018

@author: Julian
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 23:27:50 2017

@author: Julian
"""

# For Text Extraction
import pandas as pd
import bs4
import urllib

# Further Analysis
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords
import os
import pysentiment as ps



d = "C:/Users/Julian/pyning"

# Read the whole text.
cleantextprep = open(path.join(d, 'speeches.txt'), encoding = "utf8").read()



# Regex cleaning
expression = "[^a-zA-Z0-9 ]" # keep only letters, numbers and whitespace
cleantextCAP = re.sub(expression, '', cleantextprep) # apply regex
cleantext = cleantextCAP.lower() # lower case 


# Save dictionaries for wordcloud
text_file = open("Output.txt", "w")
text_file.write(str(cleantext))
text_file.close()

    


# Count and create dictionary
dat = list(cleantext.split())
dict1 = {}
for i in range(len(dat)):
    print(i)
    word = dat[i]
    dict1[word] = dat.count(word)




# Filter Stopwords
keys = list(dict1)
filtered_words = [word for word in keys if word not in stopwords.words('english')]
dict2 = dict((k, dict1[k]) for k in filtered_words if k in filtered_words)



# Resort in list
# Reconvert to dictionary
def SequenceSelection(dictionary, length, startindex = 0): # length is length of highest consecutive value vector
    
    # Test input
    lengthDict = len(dictionary)
    if length > lengthDict:
        return print("length is longer than dictionary length");
    else:
        d = dictionary
        items = [(v, k) for k, v in d.items()]
        items.sort()
        items.reverse()   
        itemsOut = [(k, v) for v, k in items]
    
        highest = itemsOut[startindex:startindex + length]
        dd = dict(highest)
        wanted_keys = dd.keys()
        dictshow = dict((k, d[k]) for k in wanted_keys if k in d)

        return dictshow;
    
dictshow = SequenceSelection(dictionary = dict2, length = 7, startindex = 0)



# Plot most frequent words
n = range(len(dictshow))
plt.bar(n, dictshow.values(), align='center')
plt.xticks(n, dictshow.keys())
plt.title("Most frequent Words")
plt.savefig("FrequentWords.png", transparent=True)

# Overview
overview =  SequenceSelection(dictionary = dict2, length = 400, startindex = 0)
nOverview = range(len(overview.keys()))
plt.bar(nOverview, overview.values(), color = "g", tick_label = "")
plt.title("Word Frequency Overview")
plt.xticks([])
#plt.savefig("overview.png")
plt.savefig("overview.png", transparent = True)
#plt.savefig('overview.png', transparent=True)

# Sentiment Analysis
hiv4 = ps.HIV4()
tokens = hiv4.tokenize(cleantext)
score = hiv4.get_score(tokens)
print(score)


# Polarity
# Formula: (Positive - Negative)/(Positive + Negative)

# Subjectivity
# Formula: (Positive + Negative)/N


