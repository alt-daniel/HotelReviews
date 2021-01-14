from sklearn import model_selection, feature_extraction, pipeline, naive_bayes, metrics
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import seaborn as sns
import matplotlib.pyplot as plt

def split_train_test(df, size, seed):
    """ Splits a dataframe into a training and test dataframe
    :param df: dataframe to split
    :return: training dataframe, test dataframe
    """
    df_train, df_test = model_selection.train_test_split(df, test_size=size, random_state=seed)
    return df_train, df_test

def create_vectorizer(feature_count=1000, ngram_range=(1, 2)):
    """ Create vectorizer object
    :param feature_count: maximum amount of features
    :param ngram_range: tuple describing what type of ngrams to use
    :return: vectorizer
    """
    vect = feature_extraction.text.TfidfVectorizer(max_features=feature_count, ngram_range=ngram_range)
    return vect

def build_model_random_forest(vectorizer, x_verbose=2):
    """ Build a random forest model
    :param vectorizer: vectorizer object
    :return: classifier model
    """
    classifier = RandomForestClassifier(n_jobs=4, verbose=x_verbose, max_depth=50, min_samples_leaf=1, min_samples_split=5)
    model = pipeline.Pipeline([("vectorizer", vectorizer),
                               ("classifier", classifier)])
    
    return model

def build_model_naive_bayes(vectorizer, x_alpha=0.01):
    """ Build a naive bayes model
    :param vectorizer: vectorizer object
    :return: classifier model
    """
    classifier = naive_bayes.BernoulliNB(alpha=x_alpha)
    model = pipeline.Pipeline([("vectorizer", vectorizer),
                               ("classifier", classifier)])
    
    return model

def build_model_logistic_regression(vectorizer):
    """ Build a classifier model
    :param vectorizer: vectorizer object
    :param alg: what classifier algorithm to use
    :return: classifier model
    """
    classifier = LogisticRegression(random_state=0, C=1.62)
    model = pipeline.Pipeline([("vectorizer", vectorizer),
                               ("classifier", classifier)])
    
    return model

def train_model(model, feature_matrix, train_values):
    """ Train classifier model
    :param model: classifier model
    :param feature_matrix: feature matrix
    :param train_values: values to train the model on
    :return: trained model
    """
    model["classifier"].fit(feature_matrix, train_values)
    return model

def test_model(model, test_review_values):
    """ Get predicted values from test set
    :param model: classifier model
    :param test_review_values: values to test with
    :return: predicted values (binary), predicted values (probability)
    """
    predicted = model.predict(test_review_values)
    predicted_prob = model.predict_proba(test_review_values)
    return predicted, predicted_prob

def get_common_metrics(test_values, predicted):
    """ Return some common classifier metrics
    :param test_values: values to test with
    :param predicted: predicted values
    :return: accuracy, precision and recall value
    """
    accuracy = metrics.accuracy_score(test_values, predicted)
    precision = metrics.precision_score(test_values, predicted)
    recall = metrics.recall_score(test_values, predicted)
    return accuracy, precision, recall


def get_auc(test_values, predicted):
    """ Get area under the curve value
    :param test_values: values to test with
    :param predicted: predicted values
    :return: auc value
    """
    auc = metrics.roc_auc_score(test_values, predicted,
                                multi_class="ovr")
    return round(auc, 2)


def get_f1_score(precision, recall):
    """ Calculate and return F1 score
    :param precision: precision score
    :param recall: recall score
    :return: F1 score
    """
    return (2 * (precision * recall)) / (precision + recall)


def plot_confusion_matrix(test_values, predicted):
    classes = [0, 1]
    cm = metrics.confusion_matrix(test_values, predicted)

    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', ax=ax, cmap=plt.cm.PuRd, cbar=False)
    ax.set(xlabel="Predicted",
           ylabel="True",
           xticklabels=classes,
           yticklabels=classes,
           title="Confusion Matrix")
    plt.yticks(rotation=0)
    plt.show()


def plot_roc_curve(test_values, predicted):
    fpr, tpr, threshold = metrics.roc_curve(test_values, predicted)
    roc_auc = metrics.auc(fpr, tpr)

    plt.title('ROC')
    plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()