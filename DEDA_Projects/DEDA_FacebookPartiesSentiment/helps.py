import requests
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import pandas as pd
import itertools
from nltk.stem.snowball import GermanStemmer
from sklearn.feature_extraction.text import CountVectorizer
import numpy
from pathlib import Path
import os

home = str(Path.home())
sep = os.sep
path = home + sep + "Downloads" + sep


# get minimum 100 messages
def get_all_messages_of_a_page(graph, page_id):
    page = graph.get_object(id=page_id, fields="posts")
    messages = []
    str_msg = "message"
    i = 0

    # get all messages out of the dict (response of API)
    for i in range(len(page["posts"]["data"])):
        if str_msg in page["posts"]["data"][i]:
            messages.append(page["posts"]["data"][i]["message"])

    i = 0
    next_page = page["posts"]["paging"]["next"]

    # loop as long as minimum 100 messages are collected
    while (len(messages) < 100):
        try:
            data = requests.get(next_page).json()

            for i in range(len(data["data"])):
                if str_msg in data["data"][i]:
                    messages.append(data["data"][i]["message"])

                next_page = data["paging"]["next"]

        except KeyError:
            print("Can't find 'next' key -- no additional page")
            break

    return messages


def clean_word_list(msg):
    sen = list()
    index = list()
    h = list()

    for message in msg:
        message = str(message)

        index.clear()
        i = -1
        b = True

        while b:
            # find the next punctuation mark
            if message.find(".", i + 1) != -1:
                h.append(message.find(".", i + 1))
            if message.find("!", i + 1) != -1:
                h.append(message.find("!", i + 1))
            if message.find("?", i + 1) != -1:
                h.append(message.find("?", i + 1))

            if h.__len__() == 0:
                i = -1
            else:
                i = min(h)

            h.clear()

            # end loop if no punctuation mark is found anymore (then i = -1)
            if i == -1:
                b = False
            # make sure that the dot is not a part of a hyperlink or of a date
            elif message[i - 3:i] != "www" and not message[i - 1].isdigit() and message[
                                                                                i + 2:message.find(" ", i + 2)] not in [
                "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober",
                "November", "Dezember"]:
                index.append(i)

        a = 0

        # put all sentences together
        for idx in index:
            tmp = message[a:idx + 1]
            a = idx + 1
            sen.append(tmp)

    r = list()

    # filter messages (stem and remove stop words)
    for elem in sen:
        message_filtered = remove_stop_words(elem)
        string = " ".join(message_filtered)
        r.append(string)
        string = ""

    data = pd.DataFrame({
        "phrase": r,
        "polarity": ""
    })

    return data


def remove_stop_words(msg):
    # remove stop words and stem words
    stemmer = GermanStemmer()

    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(msg)

    stop_words = set(stopwords.words('german'))

    words_filtered = []

    for w in words:
        if w not in stop_words:
            words_filtered.append(stemmer.stem(w))

    return words_filtered


# def getTestDataDict():
#    #get the Dictionary
#    neg = pd.read_csv(path + "SentiWS_v1.8c"+ sep + "SentiWS_v1.8c_Negative.txt",
#                          sep="\t", header=None, names=["wordplustype", "polarity", "sim"])

# prepare Dictionary
#    negativedata = prepareSentimentDict(neg)

#    pos = pd.read_csv(path + "SentiWS_v1.8c"+sep+"SentiWS_v1.8c_Positive.txt",
#                          sep="\t", header=None, names=["wordplustype", "polarity", "sim"])

#    positivedata = prepareSentimentDict(pos)

#    result = positivedata.append(negativedata, ignore_index=True)

#    return result

def prepare_sentiment_dict(data):
    combinedwords = data["wordplustype"]
    wordlist = list()
    wordtype = list()

    # seperate original word and similar words
    for combination in combinedwords:
        comb = str(combination)
        word = comb[:comb.find("|")]
        ty = comb[comb.find("|") + 1:]

        wordlist.append(word)
        wordtype.append(ty)

    tmp = pd.DataFrame(
        {"word": wordlist,
         "type": wordtype,
         "polarity": data["polarity"],
         "sim": data["sim"]}
    )

    tmp2 = tmp

    # split chain of similar words into single words
    for index, row in tmp.iterrows():
        rsim = row["sim"]
        simwords = str(rsim).split(",")

        # build the dataframe (repeat word tpye and polarity for every similar word)
        if ("nan" not in str(simwords)):
            pol = list(itertools.repeat(row["polarity"], simwords.__len__()))
            t = list(itertools.repeat(row["type"], simwords.__len__()))

            tmp3 = pd.DataFrame(
                {"polarity": pol,
                 "type": t,
                 "word": simwords
                 }
            )

            # build final dataframe
            tmp2 = tmp2.append(tmp3, ignore_index=True)

    del tmp2["sim"]
    tmp2 = tmp2[["word", "type", "polarity"]]

    return tmp2


def get_test_data_sentences():
    # get corpus of sentences
    data = pd.read_csv(path + "mlsa" + sep + "layer2.phrases.majority.txt",
                       sep="\t", header=None, names=["sentence_ID", "phrase", "type_of_phrase"])

    phrases = data.phrase
    phrase = list()
    polarity = list()

    for index, row in phrases.iteritems():
        # split sentences in phrase and polarity
        r = str(row)
        ph = r[:r.__len__() - 1]
        pol = r[r.__len__() - 1:]

        # + = pos, - = neg, 0 = neutral, # = bipolar (both negative and positive)
        # remove 0 and # since only positive and negative phrases are relevant
        if pol == "+":
            pol = 1
        elif pol == "-":
            pol = 0
        elif pol == "0":
            pol = numpy.nan
        elif pol == "#":
            pol = numpy.nan

        ph = remove_stop_words(ph)

        tmp = ""

        # concatenate the words
        for elem in ph:
            tmp = tmp + " " + elem

        phrase.append(tmp[1:])
        polarity.append(pol)

    testdata = pd.DataFrame({
        "phrase": phrase,
        "polarity": polarity,
    })

    return testdata.dropna()


# for regression modeling
def vectorize(data):
    corpus_data_features = vectorizer.fit_transform(data)
    return corpus_data_features


def tokenize(text):
    tokens = nltk.word_tokenize(text)

    return tokens


vectorizer = CountVectorizer(
    analyzer='word',
    tokenizer=tokenize,
    lowercase=True,
    max_features=350
)
