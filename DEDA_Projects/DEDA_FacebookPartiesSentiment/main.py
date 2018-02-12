import facebook
import re
import helps
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

# @TODO update token via https://developers.facebook.com/tools/explorer/145634995501895/

# build connection to Facebook's API Graph
token = "EAACEdEose0cBAAh6p4d5LaSH3PwjlXFBnHdXgg0GsQkpIdw8GZAtuMtITBXSnQzrBj9iZBrV2exMCEwmrKcwZBLlkkBJBPgIXZCPFxZAMKmnbttLakjZBzPtJmstGOAc1KqYQRIdYvr2P5z5tKP86K4Mc3sJZBwRLkewboFNDiv1bPJmPVsRV33wmhbc0axbmLmuMkIekiDxwZDZD "
graph = facebook.GraphAPI(access_token=token, version="2.11")

parties = ["CDU", "CSU (Christlich-Soziale Union)", "SPD", "Die Linke", "AfD", "BÜNDNIS 90/DIE GRÜNEN", "FDP"]
page_id = {}

# search for the page IDs of the seven big parties which are currently in the parlament (Bundestag)
for i in range(len(parties)):
    tmp = graph.search(type="page", q=parties[i])
    reg = re.compile("\\b" + parties[i] + "\\b")
    b = False
    j = 0

    while not b and (j < 10):
        if (re.search(reg, tmp["data"][j]["name"]) != "" and len(parties[i]) == len(tmp["data"][j]["name"])):

            if (parties[i] == "CSU (Christlich-Soziale Union)"):
                key = "CSU"
            elif (parties[i] == "BÜNDNIS 90/DIE GRÜNEN"):
                key = "Gruene"
            elif (parties[i] == "Die Linke"):
                key = "Linke"
            else:
                key = parties[i]

            page_id[key] = tmp["data"][j]["id"]
            b = True

        else:
            j = j + 1

print("Page IDs found")

# get minimum 100 messages of the facebook page
cdu_msg = helps.get_all_messages_of_a_page(graph, page_id["CDU"])
csu_msg = helps.get_all_messages_of_a_page(graph, page_id["CSU"])
spd_msg = helps.get_all_messages_of_a_page(graph, page_id["SPD"])
linke_msg = helps.get_all_messages_of_a_page(graph, page_id["Linke"])
fdp_msg = helps.get_all_messages_of_a_page(graph, page_id["FDP"])
afd_msg = helps.get_all_messages_of_a_page(graph, page_id["AfD"])
gruene_msg = helps.get_all_messages_of_a_page(graph, page_id["Gruene"])

print("all messages collected")

# clean messages (stem words, remove stopwords)
cdu = helps.clean_word_list(cdu_msg)
csu = helps.clean_word_list(csu_msg)
spd = helps.clean_word_list(spd_msg)
linke = helps.clean_word_list(linke_msg)
fdp = helps.clean_word_list(fdp_msg)
afd = helps.clean_word_list(afd_msg)
gruene = helps.clean_word_list(gruene_msg)

print("cleaned messages")

# get the corpusses (Dictionary and Sentences)
# testwords = helps.getTestDataDict()
testsentences = helps.get_test_data_sentences()

# vectorize the sentences of the corpus
v = helps.vectorize(testsentences.phrase)

# split corpus into train and test set
X_train, X_test, y_train, y_test = train_test_split(
    v,
    testsentences.polarity,
    train_size=0.85,
    test_size=0.15,
    random_state=1234)

# do logistic regression
print("start first logistic regression (training)")

log_model = LogisticRegression()
log_model = log_model.fit(X=X_train, y=y_train)

y_pred = log_model.predict(X_test)

# print summary of the model (contains e.g. accuracy of the model)
print(classification_report(y_test, y_pred))

# train classifier with whole corpus
print("start second logistic regression (testing)")
log_model = LogisticRegression()
log_model = log_model.fit(X=v, y=testsentences.polarity)

# get predictions
cdu_pred = log_model.predict(helps.vectorize(cdu.phrase))
csu_pred = log_model.predict(helps.vectorize(csu.phrase))
spd_pred = log_model.predict(helps.vectorize(spd.phrase))
linke_pred = log_model.predict(helps.vectorize(linke.phrase))
fdp_pred = log_model.predict(helps.vectorize(fdp.phrase))
afd_pred = log_model.predict(helps.vectorize(afd.phrase))
gruene_pred = log_model.predict(helps.vectorize(gruene.phrase))

# summarize the percentages of positive sentences
positive_sentences = []
positive_sentences.append(sum(cdu_pred) / cdu.__len__())
positive_sentences.append(sum(csu_pred) / csu.__len__())
positive_sentences.append(sum(spd_pred) / spd.__len__())
positive_sentences.append(sum(linke_pred) / linke.__len__())
positive_sentences.append(sum(fdp_pred) / fdp.__len__())
positive_sentences.append(sum(afd_pred) / afd.__len__())
positive_sentences.append(sum(gruene_pred) / gruene.__len__())

# summarize the persentages of negative sentences
negative_sentences = []
negative_sentences.append((cdu.phrase.__len__() - sum(cdu_pred)) / cdu.__len__())
negative_sentences.append((csu.phrase.__len__() - sum(csu_pred)) / csu.__len__())
negative_sentences.append((spd.phrase.__len__() - sum(spd_pred)) / spd.__len__())
negative_sentences.append((linke.phrase.__len__() - sum(linke_pred)) / linke.__len__())
negative_sentences.append((fdp.phrase.__len__() - sum(fdp_pred)) / fdp.__len__())
negative_sentences.append((afd.phrase.__len__() - sum(afd_pred)) / afd.__len__())
negative_sentences.append((gruene.phrase.__len__() - sum(gruene_pred)) / gruene.__len__())

# plot this
X = range(7)
p1 = plt.bar(X, negative_sentences, color='#F20000')

axes = plt.gca()
axes.set_ylim([0, 1])

plt.ylabel('Messages with negative Sentiment in %')
plt.title('Sentiment of facebook posts written by political parties')
plt.xticks(X, ("CDU", "CSU", "SPD", "Linke", "FDP", "AFD", "Grüne"))

for a, b in zip(X, negative_sentences):
    plt.text(a, b, str(round(b, 2)), ha="center")

plt.show()
plt.savefig(fname="C:\\Users\\Christine\\Desktop\\Studium\\DEDA\\Sentiments.png")
