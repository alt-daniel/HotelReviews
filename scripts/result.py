import numpy as np
import pandas as pd
import os
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

import sys
sys.path.append('../')
from util.file_util import pickle_to_dataframe
from config import MERGED_REVIEWS_PATH

# WordCloud

df = pd.read_pickle('/Users/daniel/Documents/BigData/Hotel_Reviews/static/pickle/merged_pickle.pkl')

positive_df = df[df.is_positive == 1 ]
negative_df = df[df.is_positive == 0 ]

positive_text = " ".join(review for review in positive_df.review)
negative_text =  " ".join(review for review in negative_df.review)

pos_wordcloud = WordCloud().generate(positive_text)
neg_wordcloud = WordCloud(background_color='white').generate(negative_text)

# Worldclouds
plt.imshow(pos_wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

plt.imshow(neg_wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

df_grouped = df.groupby(['nation']).size().nlargest(5)
df_grouped = df_grouped.reset_index(name='count')

ax = df_grouped.plot.bar(x='nation', y='count', rot=90)

