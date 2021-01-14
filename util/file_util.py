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


def pickle_model(model, destination):
    """
    Pickled and writes an object to a file as long as the file doesn't exist
    :param object_to_dump: object that will be written
    :param filepath: where the file is
    """
    if os.path.isfile(destination):
        pass
    else:
        with open(destination, 'wb') as f:
            pickle.dump(model, f)

def get_pickled_object(source):
    """
    Reads from a file and unpickles the stored object
    :param filepath: where the file is
    :return: unpickled object
    """
    with open(source, 'rb') as f:
        try:
            unpickled_object = pickle.load(f)
            return unpickled_object
        except pickle.UnpicklingError as e:
            raise e