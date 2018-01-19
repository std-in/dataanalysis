# -*- coding: utf-8 -*-
# -*- coding: <encoding name> -*-

import numpy as np
import sys
import re
import codecs
import os
import jieba
import gensim, logging
from gensim.models import word2vec
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib
from sklearn.preprocessing import scale
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from scipy import stats
from sklearn.cross_validation import train_test_split
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Activation
# from keras.optimizers import SGD
from sklearn.metrics import f1_score
# from bayes_opt import BayesianOptimization as BO
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
import sklearn
from sklearn.metrics import roc_auc_score as auc
from sklearn.metrics import accuracy_score as acc


def parseSent(sentence):
    seg_list = jieba.cut(sentence)
    output = ''.join(list(seg_list))  # use space to join them
    return output


def sent2word(sentence):
    """
    Segment a sentence to words
    Delete stopwords
    """
    segResult = []
    segList = jieba.cut(''.join(re.findall(u'[\u4e00-\u9fff]+', sentence)))
    for w in segList:
        segResult.append(w)
    stopwords = readLines('/home/nyh/work/workspace/dataanalysis/dmlib/data/nlp/stopWords.txt')
    newSent = []
    stopwords_list = []
    for word in segResult:
        if word in stopwords:
            # print "stopword: %s" % word
            continue
        else:
            newSent.append(word)
    # output = ' '.join(list(newSent))
    return newSent


def eachFile(filepath):
    pathDir = os.listdir(filepath)
    child = []
    for allDir in pathDir:
        child.append(os.path.join('%s/%s' % (filepath, allDir)))
    return child


def readLines(filename):
    fopen = open(filename, 'r')
    data = []
    for x in fopen.readlines():
        if x.strip() != '':
            data.append(x.strip())
    fopen.close()
    return data


def readFile(filename):
    data = []
    for x in filename:
        fopen = open(x, 'r')
        for eachLine in fopen:
            if eachLine.strip() != '':
                data.append(eachLine.strip())
    fopen.close()
    return data


def getWordVecs(wordList):
    vecs = []
    for word in wordList:
        word = word.replace('\n', '')
        try:
            vecs.append(model[word])
        except KeyError:
            continue
    return np.array(vecs, dtype = 'float')


def buildVecs(filename):
    posInput = []
    with open(filename, "r", encoding = "utf-8") as txtfile:
        for lines in txtfile:
            lines = lines.split('\n')
            if lines[0] == "\r" or lines[0] == "\r\n" or lines[0] == "\r\r":
                pass
            else:

                for line in lines:
                    line = list(jieba.cut(line))

                    resultList = getWordVecs(line)

                    # for each sentence, the mean vector of all its vectors is used to represent this sentence
                    if len(resultList) != 0:
                        resultArray = sum(np.array(resultList)) / len(resultList)
                        posInput.append(resultArray)

    return posInput


# load word2vec model
# 训练模型输出模型
os.chdir("/home/nyh/work/workspace/dataanalysis/dmlib/")
filepwd = eachFile("/home/nyh/work/workspace/dataanalysis/dmlib/data/nlp/test")
sentences = []
for x in filepwd:
    data = readLines(x)
    for line in data:
        sentences.extend(sent2word(line))
    # sentences.append(data[0])

model = gensim.models.Word2Vec(sentences, min_count=0, size = 500)
# outp1 = 'corpus.model.bin'
# model.save(outp1)

filepwd_pos = eachFile('../data/pos')
filepwd_neg = eachFile('../data/neg')

pos_number = 0
neg_number = 0
posInput = []
negInput = []
for pos in filepwd_pos:
    pos_buildVecs = buildVecs(pos)
    posInput.extend(pos_buildVecs)
    pos_number += 1
    if pos_number == 100:
        break
for neg in filepwd_neg:
    neg_buildVecs = buildVecs(neg)
    negInput.extend(neg_buildVecs)
    neg_number += 1
    if neg_number == 100:
        break

y = np.concatenate((np.ones(len(posInput)), np.zeros(len(negInput))))

X = posInput[:]

for neg in negInput:
    X.append(neg)

X = np.array(X)

X = scale(X)

X_reduced = PCA(n_components=100).fit_transform(X)

# X_reduced_train,X_reduced_test, y_reduced_train, y_reduced_test =train_test_split(X_reduced,y)


X_reduced_train, X_reduced_test, y_reduced_train, y_reduced_test = train_test_split(X_reduced, y, test_size=0.4,
                                                                                    random_state=1)

"""
SVM (RBF)
    using training data with 100 dimensions
"""

clf = SVC(C=2, probability=True)
clf.fit(X_reduced_train, y_reduced_train)
print
'Test Accuracy: %.2f' % clf.score(X_reduced_test, y_reduced_test)

pred_probas = clf.predict_proba(X_reduced_test)[:, 1]

# print "KS value: %f" % KSmetric(y_reduced_test, pred_probas)[0]

# plot ROC curve# AUC = 0.92# KS = 0.7


# 输出相关结果 以及绘图
print("test:")
print(clf.predict(X_reduced_test))
print("value:")
print(y_reduced_test)

test_value = clf.predict(X_reduced_test)

index = []
for x in range(0, len(test_value)):
    index.append(x + 1)

test_value_1 = 0
test_value_0 = 0
for test_value_data in test_value:
    if test_value_data == 1:
        test_value_1 += 1
    else:
        test_value_0 += 1

y_reduced_test_1 = 0
y_reduced_test_0 = 0
for y_reduced_test_data in y_reduced_test:
    if y_reduced_test_data == 1:
        y_reduced_test_1 += 1
    else:
        y_reduced_test_0 += 1

test_value_label = 'test pos: ' + str(test_value_1) + ' neg: ' + str(test_value_0)
y_reduced_test_label = 'value pos: ' + str(y_reduced_test_1) + ' neg: ' + str(y_reduced_test_0)

plt.plot(index, test_value, 'ro', label=test_value_label)
plt.plot(index, y_reduced_test, 'b.', label=y_reduced_test_label)
plt.xlim([0, len(test_value)])
plt.ylim([-2, 2])
plt.legend(loc='lower right')
plt.show()

fpr, tpr, _ = roc_curve(y_reduced_test, pred_probas)
roc_auc = sklearn.metrics.auc(fpr, tpr)
plt.plot(fpr, tpr, label='roc_auc = %.2f' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.legend(loc='lower right')
plt.show()