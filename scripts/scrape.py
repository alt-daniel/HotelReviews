import sys
sys.path.append('../')
from util.file_util import csv_to_dataframe
from config import SCRAPED_RAW_REVIEWS_PATH
import pandas as pd
from langdetect import detect

raw_df = csv_to_dataframe(SCRAPED_RAW_REVIEWS_PATH)
df2 = raw_df.copy()
default_empty_value = ['n/a', 'nothing']


def split_review(target_df):
    """
    Split the negative reviews and the positive reviews in 2 rows. 
    Add a new column that says if the review is positive

    Args:
        target_df (DataFrame): The original dataframe.
    
    Returns:
        Returns a new dataframe with 2 new columns.
    """

    cols = ['hotel_name', 'nation', 'review', 'is_positive', 'score', 'title']
    df = pd.DataFrame()

    for index, row in target_df.iterrows():
        df = df.append([[row.hotel_name, row.nation, row.positive_review, 1, row.score,row.title]], ignore_index=True)
        df = df.append([[row.hotel_name, row.nation, row.negative_review, 0, row.score,row.title]], ignore_index=True)
        
    df.columns = cols

    return df


def drop_empty_reviews(df, empty_values=['n/a', 'nothing']):
    """Drops empty reviews and rows with default values

    Args:
        df (DataFrame): The raw dataframe with empty reviews
        empty_values (list, optional): List of strings that should be deleted. Defaults to ['n/a', 'nothing'].

    Returns:
        DataFrame: Dataframe without the empty reviews
    """
    #Drop empty rows
    df.dropna(subset=['review'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    #Remove with a certain value
    df['review'] = df['review'].str.strip()
    df.drop(df[df['review'].str.lower().isin(empty_values)].index, inplace=True)

    return df
df2 = split_review(df2)
df2 = drop_empty_reviews(df2)
row38 = df2.iloc[38].review
langcode = detect(row38)


# Remove rows with empty reviews and default value
# df = df.dropna(subset=['review'])
# df3.dropna(subset=['review'], inplace=True)
# df3.reset_index(drop=True, inplace=True)
# # df = df.drop(df[df['review'] == default_empty_value].index)
# df['review'] = df['review'].str.strip()
# df.drop(df[df['review'].str.lower().isin(default_empty_value)].index, inplace=True)




