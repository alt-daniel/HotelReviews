from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
import pandas as pd
from config import HOST, USERNAME, PASSWORD, DATABASE

def create_connection():
    """
    Create database connection
    :return: connection object
    """
    try:
        # Take not that you'll HAVE TO set your database charset to utf8mb4, otherwise you'll not be able to call
        # df_to_db(), due to encoding issues
        # engine = create_engine(f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}")
        engine = create_engine('mysql+mysqlconnector://tester:test@localhost/hotel_reviews')  

        connection = engine.connect()
        return connection
    except DatabaseError as e:
        print(f"Database error: {e}")




def df_to_db(df, connection=create_connection()):
    """
    Transfers the review dataframe to the connected database
    :param df: dataframe
    :param connection: connection object
    """
    df.to_sql("reviews", connection, if_exists='append', index=True, chunksize=5000)


def db_to_df(nrows, connection=create_connection()):
    """
    Transfer results of a SQL query to a dataframe
    :param amount: limit amount of entries returned
    :param connection: connection object
    :return: dataframe
    """
    query = pd.read_sql(f"CALL get_reviews(%(nrows)s)", connection, params={"nrows": nrows})
    df = pd.DataFrame(query)
    return df

