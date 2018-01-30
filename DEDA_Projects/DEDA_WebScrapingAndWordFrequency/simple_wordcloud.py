# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 20:09:46 2017

@author: Julian
"""

from os import path
from wordcloud import WordCloud

d = "C:/Users/Julian/pyning"

# Read the whole text.
text = open(path.join(d, 'Output.txt')).read()

# Generate a word cloud image
wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
plt.savefig("Simple_Wordcloud.png")

# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()