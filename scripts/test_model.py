import sys
sys.path.append('../')
from util.train_util import *
from util.database_util import create_connection, df_to_db, db_to_df
from util.file_util import pickle_to_dataframe, get_pickled_object, pickle_model
from config import MERGED_REVIEWS_PATH, RANDOM_FOREST_MODEL_PATH, LOGISTIC_REGRESSION_MODEL_PATH, NAIVE_BAYES_MODEL_PATH
from sklearn import model_selection, feature_extraction, pipeline, naive_bayes, metrics
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
import seaborn as sns


model = get_pickled_object(LOGISTIC_REGRESSION_MODEL_PATH)

print("Calculating metrics ..")
predicted, predicted_prob = test_model(model, df_test["review"].values)
accuracy, precision, recall = get_common_metrics(test_labels, predicted)
f1 = get_f1_score(precision, recall)
auc = get_auc(test_labels, predicted)
plot_confusion_matrix(test_labels, predicted)
plot_roc_curve(test_labels, predicted)

print(f"Accuracy: {accuracy} | Precision: {precision} | Recall: {recall}")
print(f"F1 score: {f1}")
print(f"AUC: {auc}")