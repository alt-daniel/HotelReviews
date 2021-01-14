import pandas as pd
from pymongo import MongoClient


# # Load csv dataset
#     data = pd.read_csv('<<INSERT NAME OF DATASET>>.csv')

def create_mongodb_connection(df):
    # Connect to MongoDB
    # client =  MongoClient("mongodb///?Server=localhost&Port=27017&Database=Hotel_Reviews&User=root&Password=zaqwerty353")
    client =  MongoClient("mongodb://localhost:27017")

    db = client['Hotel_Reviews']
    collection = db['Cleaned_Reviews']

    df.reset_index(inplace=True)
    data_dict = df.to_dict("records")
    collection.insert_many(data_dict)


def mongodb_to_df(limit=None):
    client =  MongoClient("mongodb://localhost:27017")

    db = client['Hotel_Reviews']
    collection = db['Cleaned_Reviews']
    df=pd.DataFrame()

    if limit is not None:
        df = pd.DataFrame(list(collection.find().limit(limit)))
    else:
        df = pd.DataFrame(list(collection.find()))
    
    df.drop(columns=['_id'])
    return df
