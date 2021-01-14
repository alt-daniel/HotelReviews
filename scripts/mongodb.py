import sys
sys.path.append('../')

# from util.database_util import create_connection, df_to_db, db_to_df
# df = db_to_df(306000)
# df_cleaned = df.drop(columns=['index'])
# create_mongodb_connection(df_cleaned)

from util.mongodb_util import create_mongodb_connection, mongodb_to_df

df_from_db = mongodb_to_df(10000)
df = df_from_db.drop(columns=['_id'])
print(df_from_db.head())

from dask.distributed import Client, progress
client = Client(n_workers=2, threads_per_worker=2, memory='2GB')


import dask.dataframe as dd
dask_df = dd.from_pandas(df, npartitions=3)


#  # Get sentiment values
# print("Retrieving sentiment values...\n")
# train_labels = df_train['is_positive'].values
# test_labels = df_test['is_positive'].values

df_train, df_test = dask_df.random_split([0.5, 0.5])

import dask_ml.feature_extraction.text
vect = dask_ml.feature_extraction.text.HashingVectorizer()
x_train = vect.fit_transform(df_train['review'])
