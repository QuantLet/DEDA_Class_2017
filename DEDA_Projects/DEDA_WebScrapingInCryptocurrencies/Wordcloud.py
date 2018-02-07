'''
Wordcloud
'''


from collections import Counter
from wordcloud import WordCloud
from PIL import Image

def wordcloud(text,image):

    picture = np.array(Image.open(image))

    wc = WordCloud(background_color="rgba(255, 255, 255, 0)", mode="RGBA",
                   mask = picture,
                   max_words = 1000)
    wc.generate_from_frequencies(text)

    wc.to_file("btc_wordcloud_2.png")


counts = dict(Counter(word_list).most_common(1000))
wc = wordcloud(counts,"btc_white.jpg")



