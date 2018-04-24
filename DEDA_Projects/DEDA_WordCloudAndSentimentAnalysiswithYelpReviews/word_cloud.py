# further information about wordcloud go to https://github.com/amueller/word_cloud

from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt

reviews_df = pd.read_csv("Reviews.csv", sep=',', encoding='cp1251')
description_list = reviews_df.Review.values
text = str(description_list)
# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
