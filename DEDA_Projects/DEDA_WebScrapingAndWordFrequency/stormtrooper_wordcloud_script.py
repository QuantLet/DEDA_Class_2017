# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 20:19:52 2017

@author: Julian
@modified by: Junjie Hu, 02.05.2018
"""

from os import path
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

root_path = os.getcwd()

# Read the whole text.
with open(path.join(root_path, 'Output.txt'), 'r', encoding='utf-8', errors='ignore') as outout_file:
    text = outout_file.readlines()

# Mask
stormtrooper_mask = np.array(Image.open(path.join(root_path, "stormtrooper_mask.png")))

# Optional additional stopwords
stopwords = set(STOPWORDS)
stopwords.add("said")

# Construct Word Cloud
# no backgroundcolor and mode = 'RGBA' create transparency
wc = WordCloud(max_words=1000, mask=stormtrooper_mask,
               stopwords=stopwords, mode='RGBA', background_color=None)

# Pass Text
wc.generate(text[0])

# store to file
wc.to_file(path.join(root_path, "stormtrooper.png"))

# show
# plt.figure()
# plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# plt.imshow(stormtrooper_mask, cmap=plt.cm.gray, interpolation='bilinear')
# plt.axis("off")
# plt.savefig("stormtrooper.png")
# plt.show()
