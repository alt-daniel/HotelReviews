import sys
sys.path.append('../')
from util.file_util import csv_to_dataframe
from config import SCRAPED_RAW_REVIEWS_PATH

df = csv_to_dataframe(SCRAPED_RAW_REVIEWS_PATH)
df2 = df.head(5).copy()

# import pandas as pd
cols = ['hotel_name', 'nation', 'review', 'is_positive', 'score', 'title']
df3 = pd.DataFrame()
for index, row in df2.iterrows():
    df3 = df3.append([[row.hotel_name, row.nation, row.positive_review, 1, row.score,row.title]], ignore_index=False)
    df3 = df3.append([[row.hotel_name, row.nation, row.negative_review, 0, row.score,row.title]], ignore_index=False)
df3.columns = cols


