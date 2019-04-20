# coding=gbk

import time
from sklearn import metrics
import pickle as pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Multinomial Naive Bayes Classifier
def naive_bayes_classifier(train_x, train_y):
    from sklearn.naive_bayes import MultinomialNB
    model = MultinomialNB(alpha=0.01)
    model.fit(train_x, train_y)
    return model


# KNN Classifier
def knn_classifier(train_x, train_y):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier()
    model.fit(train_x, train_y)
    return model


# Logistic Regression Classifier
def logistic_regression_classifier(train_x, train_y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty='l2')
    model.fit(train_x, train_y)
    return model


# Random Forest Classifier
def random_forest_classifier(train_x, train_y):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=8)
    model.fit(train_x, train_y)
    return model


# Decision Tree Classifier
def decision_tree_classifier(train_x, train_y):
    from sklearn import tree
    model = tree.DecisionTreeClassifier()
    model.fit(train_x, train_y)
    return model


# GBDT(Gradient Boosting Decision Tree) Classifier
def gradient_boosting_classifier(train_x, train_y):
    from sklearn.ensemble import GradientBoostingClassifier
    model = GradientBoostingClassifier(n_estimators=200)
    model.fit(train_x, train_y)
    return model


# SVM Classifier
def svm_classifier(train_x, train_y):
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    model.fit(train_x, train_y)
    return model


# SVM Classifier using cross validation
def svm_cross_validation(train_x, train_y):
    from sklearn.model_selection import GridSearchCV
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True,gamma='scale')
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}
    grid_search = GridSearchCV(model, param_grid, n_jobs=1, verbose=1)
    grid_search.fit(train_x, train_y)
    best_parameters = grid_search.best_estimator_.get_params()
    for para, val in list(best_parameters.items()):
        print(para, val)
    model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
    model.fit(train_x, train_y)
    return model


def read_data(data_file):
    data = pd.read_csv(data_file)
    train = data[:int(len(data) * 0.9)]
    test = data[int(len(data) * 0.9):]
    train_y = train.label
    train_x = train.drop('label', axis=1)
    test_y = test.label
    test_x = test.drop('label', axis=1)
    return train_x, train_y, test_x, test_y


if __name__ == '__main__':

    with open('C:/Users/win8/PycharmProjects/textmining/venv/1111stop.txt', encoding='utf8') as file:
        stopWord_list = [k.strip() for k in file.readlines()]
    train_df = pd.read_csv('C:/Users/win8/PycharmProjects/textmining/venv/train.txt', sep='\t', header=None, )
    train_df = train_df.astype(str)
    train_df.shape
    import jieba
    train_df.columns = ['分类', '文章']
    stopword_list = [k.strip() for k in open('C:/Users/win8/Desktop/1111stop.txt', encoding='utf8').readlines() if
                     k.strip() != '']
    cutWords_list = []
    i = 0
    startTime = time.time()
    for article in train_df['文章']:
        cutWords = [k for k in jieba.cut(article) if k not in stopword_list]
        i += 1
        if i % 1000 == 0:
            print('前%d篇文章分词共花费%.2f秒' % (i, time.time() - startTime))
        cutWords_list.append(cutWords)
    with open('C:/Users/win8/PycharmProjects/textmining/venv/cutWords_list.txt', 'w', encoding='utf-8') as file:
        for cutWords in cutWords_list:
            file.write(' '.join(cutWords) + '\n')
    with open('C:/Users/win8/PycharmProjects/textmining/venv/cutWords_list.txt', encoding='utf-8') as file:
        cutWords_list = [k.split() for k in file.readlines()]
    tfidf = TfidfVectorizer(cutWords_list, min_df=40, max_df=0.3)
    X = tfidf.fit_transform(train_df['文章'])
    print(X.shape)

    train_df = pd.read_csv('C:/Users/win8/PycharmProjects/textmining/venv/train.txt', sep='\t', header=None)
    train_df = train_df.astype(str)
    labelEncoder = LabelEncoder()
    y = labelEncoder.fit_transform(train_df[0].values)
    y.shape
    print(train_df[0].value_counts())

    print('reading training and testing data...')
    train_x,test_x,train_y,test_y=train_test_split(X, y, test_size=0.2)
    thresh = 0.5
    model_save_file = 'C:/Users/win8/PycharmProjects/textmining/venv/lr_40_0.3.model'
    model_save = {}


    test_classifiers = ['NB', 'KNN', 'LR', 'RF', 'DT', 'SVM', 'SVMCV', 'GBDT']
    classifiers = {'NB': naive_bayes_classifier,
                   'KNN': knn_classifier,
                   'LR': logistic_regression_classifier,
                   'RF': random_forest_classifier,
                   'DT': decision_tree_classifier,
                   'SVM': svm_classifier,
                   'SVMCV': svm_cross_validation,
                   'GBDT': gradient_boosting_classifier
                   }

    for classifier in test_classifiers:
        print('******************* %s ********************' % classifier)
        start_time = time.time()
        model = classifiers[classifier](train_x, train_y)
        print('training took %fs!' % (time.time() - start_time))
        predict = model.predict(test_x)
        if model_save_file != None:
            model_save[classifier] = model
        precision = metrics.precision_score(test_y, predict, average='macro')
        recall = metrics.recall_score(test_y, predict, average='macro')
        print('precision: %.2f%%, recall: %.2f%%' % (100 * precision, 100 * recall))
        accuracy = metrics.accuracy_score(test_y, predict)
        print('accuracy: %.2f%%' % (100 * accuracy))

    if model_save_file != None:
        pickle.dump(model_save, open(model_save_file, 'wb'))