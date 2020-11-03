import pickle
from config
import pandas as pd 
import os

def csv_to_dataframe(source):
    try: 
        df = pd.read_csv(source, headers=True)
        return df
    except IOError as e:
        print(e)

def pickle_to_dataframe(source):
    try: 
        df = pd.read_pickle(source)
        return df
    except IOError as e:
        print(e)

def dataframe_to_csv(dataframe, destination):
    dataframe.dataframe_to_csv(destination, header=True)

def dataframe_to_pickle(dataframe, destination):
    dataframe.to_pickle(destination, header=True)
    