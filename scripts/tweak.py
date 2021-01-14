import sys
sys.path.append('../')
from util.database_util import create_connection, df_to_db, db_to_df
from util.train_util import *
from util.file_util import pickle_to_dataframe, pickle_model, get_pickled_object
from config import RANDOM_FOREST_MODEL_PATH, LOGISTIC_REGRESSION_MODEL_PATH, NAIVE_BAYES_MODEL_PATH
from sklearn import model_selection, feature_extraction, pipeline, naive_bayes, metrics
from sklearn.model_selection import GridSearchCV
import numpy as np


df = db_to_df(100000)

df_train, df_test = split_train_test(df, 0.3, 5)
vectorizer = create_vectorizer()

 # Get sentiment values
print("Retrieving sentiment values...\n")
train_labels = df_train['is_positive'].values
test_labels = df_test['is_positive'].values

# Create feature matrix
print("Building feature matrix...\n")
vectorizer = create_vectorizer()
feature_matrix = vectorizer.fit_transform(df_train['review'])

# Select model
# Uncomment the algorithm and grid variable of choice to tweak different models

# Naive Bayes
# grid = {'classifier__alpha': [0.01, 0.1, 0.25, 0.5, 1.0]}

# Log Regression
# grid = {'classifier__C' : np.logspace(-4, 4, 20) }

# Random Forest
grid = {'classifier__max_depth': [10, 20, 30, 40, 50],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__min_samples_leaf': [1, 2, 4]}

print('Building model ..')
model = build_model_logistic_regression(vectorizer)

print("Grid searching ..")
param_search = GridSearchCV(estimator=model, param_grid=grid, verbose=2, n_jobs=4)
param_search.fit(df_train['review'], train_labels)

print("Best Parameters ..")
print(param_search.best_params_)