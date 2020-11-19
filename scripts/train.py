import sys
sys.path.append('../')
from util.train_util import *
from util.database_util import create_connection, df_to_db, db_to_df
from util.file_util import pickle_to_dataframe, pickle_model
from config import MERGED_REVIEWS_PATH, RANDOM_FOREST_MODEL_PATH, LOGISTIC_REGRESSION_MODEL_PATH, NAIVE_BAYES_MODEL_PATH
from sklearn import model_selection, feature_extraction, pipeline, naive_bayes, metrics
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
import seaborn as sns

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

print('---- Building model ----')
model = build_model_logistic_regression(vectorizer)

print('---- train model ----')
model = train_model(model, feature_matrix, train_labels)
print('Saved model to ' + NAIVE_BAYES_MODEL_PATH)
pickle_model(model, LOGISTIC_REGRESSION_MODEL_PATH)

# Test classifier
print("Calculating model metrics...\n")
predicted, predicted_prob = test_model(model, df_test["review"].values)
accuracy, precision, recall = get_common_metrics(test_labels, predicted)
f1 = get_f1_score(precision, recall)
auc = get_auc(test_labels, predicted)
plot_confusion_matrix(test_labels, predicted)
plot_roc_curve(test_labels, predicted)

print(f"Accuracy: {accuracy} | Precision: {precision} | Recall: {recall}")
print(f"F1 score: {f1}")
print(f"AUC: {auc}")