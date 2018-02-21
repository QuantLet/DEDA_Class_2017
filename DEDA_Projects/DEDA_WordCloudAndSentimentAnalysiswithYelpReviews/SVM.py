import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix



reviews_df = pd.read_csv('Reviews_all_berlin.csv', encoding = 'cp1252')


# get only reviews text and rating stars
reviews_df = reviews_df[['Restaurant Name', 'Review Rating', 'Review']]
# print(reviews_df.head())
#
# print(reviews_df['Review'][0])
# print(reviews_df['Review Rating'][0])

# print(reviews_df['Review Rating'].value_counts())
reviews_df = reviews_df[reviews_df['Review Rating'].isin([1,2,5])]
print(reviews_df['Review Rating'].value_counts())

# encode the rating to dummies, 1: 5 stars, 0: 1 and 2 stars
reviews_df['Sentiment'] = np.where(reviews_df['Review Rating']==5, 1, 0)
print(reviews_df.head())

# split train/test subset
reviews_train, reviews_test = train_test_split(reviews_df, test_size=0.1, random_state=12)
print(reviews_train.head(), reviews_test.head())

# define label list
reviews_train_label = reviews_train['Sentiment']
reviews_test_label = reviews_test['Sentiment']

# Vectorization(TF-IDF)
vectorizer = TfidfVectorizer(min_df=5,
                             max_df = 0.9,
                             sublinear_tf=True,
                             use_idf=True)

train_vectors = vectorizer.fit_transform(reviews_train['Review'])
test_vectors = vectorizer.transform(reviews_test['Review'])

# Perform classification with SVM, kernel=rbf
classifier_rbf = svm.SVC(kernel='rbf')
t0 = time.time()
classifier_rbf.fit(train_vectors, reviews_train_label)
t1 = time.time()
prediction_rbf = classifier_rbf.predict(test_vectors)
t2 = time.time()

time_rbf_train = t1-t0
time_rbf_predict = t2-t1

# Perform classification with SVM, kernel=linear
classifier_linear = svm.SVC(kernel='linear')
t3 = time.time()
classifier_linear.fit(train_vectors, reviews_train_label)
t4 = time.time()
prediction_linear = classifier_linear.predict(test_vectors)
t5 = time.time()

time_linear_train = t4-t3
time_linear_predict = t5-t4

# print the prediction results
print("Results for SVC(kernel=rbf)")
print("Training time: %fs; Prediction time: %fs" % (time_rbf_train, time_rbf_predict))
print(confusion_matrix(reviews_test_label, prediction_rbf))
print(classification_report(reviews_test_label, prediction_rbf))

print("Results for SVC(kernel=linear)")
print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
print(confusion_matrix(reviews_test_label, prediction_linear))
print(classification_report(reviews_test_label, prediction_linear))

reviews_test['predicted'] = prediction_linear
conflicts = reviews_test[reviews_test['Sentiment'] != reviews_test['predicted']]
print(conflicts)

review_info_df = pd.DataFrame(conflicts, columns=['Restaurant Name', 'Review Rating', 'Review', 'Sentiment','predicted'])
review_info_df.to_csv(os.getcwd() + '/Reviews_conflicts.csv', index=False)







