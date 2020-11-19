import sys
sys.path.append('../')
from util.database_util import create_connection, df_to_db
from util.file_util import csv_to_dataframe 
from config import SCRAPED_RAW_REVIEWS_PATH, KAGGLE_SET_PATH, MANUAL_REVIEWS_PATH
import pandas as pd
from langdetect import detect
import re
import numpy as np
import nltk

nltk.download('stopwords')
nltk.download('wordnet')
stopwords = nltk.corpus.stopwords.words("english")


default_empty_value = ['na', 'nothing', 'none', 'nan']


def split_review_and_label(target_df):
    """
    Split the negative reviews and the positive reviews in 2 rows. 
    Add a new column that says if the review is positive

    Args:
        target_df (DataFrame): The original dataframe.
    
    Returns:
        Returns a new dataframe with 2 new columns.
    """

    cols = ['hotel_name', 'nation', 'review', 'is_positive', 'score']
    df = pd.DataFrame()

    for index, row in target_df.iterrows():
        df = df.append([[row.hotel_name, row.nation, row.positive_review, 1, row.score]], ignore_index=True)
        df = df.append([[row.hotel_name, row.nation, row.negative_review, 0, row.score]], ignore_index=True)
        
    df.columns = cols

    return df

def basic_cleaning_text(text):
    if text is not None and text is not '':
        text = re.sub(r'[^\w\s]', '', str(text).lower().strip())

    return text 


def drop_empty_reviews(df, empty_values=['n/a', 'nothing',]):
    """
    Drops empty reviews and rows with default values

    Args:
        df (DataFrame): The raw dataframe with empty reviews
        empty_values (list, optional): List of strings that should be deleted. Defaults to ['n/a', 'nothing'].

    Returns:
        DataFrame: Dataframe without the empty reviews
    """
    #Remove with a certain value
    df['review'] = df['review'].apply(basic_cleaning_text)
    df.drop(df[df['review'].str.lower().isin(empty_values)].index, inplace=True)
      #Drop empty rows
    df['review'].replace('', np.nan, inplace=True)
    df.dropna(subset=['review'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df
    


def is_in_english(text):
    """
    Checks if the text is in English

    Args:
        text (str): The text that is checked on
    """
    try :
        return True if detect(text) == 'en' else False
    except: 
        return False


def final_clean(text):
    # Tokenize
    text = text.split()
    # Remove stopwords
    text = [string for string in text if string not in stopwords]
    # Lemmatize
    lem = nltk.stem.wordnet.WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text]
    text = " ".join(text)
    
    return text


# Scraped reviews
raw_df = csv_to_dataframe(SCRAPED_RAW_REVIEWS_PATH)
df2 = raw_df.copy()
del df2['title']


# Kaggle set
df3 = pd.read_csv(KAGGLE_SET_PATH, nrows=200000, index_col=False)
# only columns needed
df3 = df3[['Hotel_Name', 'Reviewer_Nationality', 'Reviewer_Score', 'Positive_Review', 'Negative_Review']]
df3.columns = ['hotel_name', 'nation', 'score', 'positive_review', 'negative_review']

#manual reviews
man_df = csv_to_dataframe(MANUAL_REVIEWS_PATH)

# Merge sets
target_cols = ['hotel_name', 'nation', 'score', 'positive_review', 'negative_review']
df2_and_man_df = pd.merge(df2, man_df, how='outer', on=target_cols)
merged_df = pd.merge(df2_and_man_df, df3, how='outer', on=target_cols)

#Cleaning
merged_df = split_review_and_label(merged_df)
merged_df = drop_empty_reviews(merged_df, default_empty_value)
merged_df = merged_df[merged_df['review'].apply(lambda x: is_in_english(x))]
merged_df['review'] = merged_df['review'].apply(final_clean)

#To database
df_to_db(merged_df)

