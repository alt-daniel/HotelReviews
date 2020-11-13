import pickle
import pandas as pd 
import os

def csv_to_dataframe(source):
    try: 
        df = pd.read_csv(source, index_col=[0])
        print("works")
        return df
    except IOError as e:
        print(e)

def pickle_to_dataframe(source):
    try: 
        df = pd.read_pickle(source, index_col=[0])
        return df
    except IOError as e:
        print(e)

def dataframe_to_csv(dataframe, destination):
    dataframe.dataframe_to_csv(destination, header=True)

def dataframe_to_pickle(dataframe, destination):
    dataframe.to_pickle(destination, header=True)
    