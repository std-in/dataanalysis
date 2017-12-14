# coding=utf-8
import os
import sys
import numpy as np
import matplotlib
import scipy
import matplotlib.pyplot as plt
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import matplotlib.pyplot as plt
import jieba
import re
import lda

# from lda import lda.datasets

trainfile = '/home/nyh/work/workspace/dataanalysis/dmlib/data/news/all'

if __name__ == "__main__":

    # 存储读取语料 一行预料为一个文档
    corpus = []
    for line in open(trainfile, 'r').readlines():
        newline = [' '.join(jieba.cut(''.join(re.findall(u'[\u4e00-\u9fff]+', line))))]
        corpus.append(line.strip())
        # print corpus

    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()
    print(vectorizer)

    X = vectorizer.fit_transform(corpus)
    analyze = vectorizer.build_analyzer()
    weight = X.toarray()

    print(str(weight))
    print(weight[:5, :5])

    # LDA算法
    print('LDA:')

    model = lda.LDA(n_topics=2, n_iter=500, random_state=1)
    model.fit_transform(X)
    # model.fit(np.asarray(weight))
    topic_word = model.topic_word_  # model.components_ also works

    # 文档-主题（Document-Topic）分布
    doc_topic = model.doc_topic_
    print("type(doc_topic): {}".format(type(doc_topic)))
    print("shape: {}".format(doc_topic.shape))

    # 输出前10篇文章最可能的Topic
    label = []
    for n in range(10):
        topic_most_pr = doc_topic[n].argmax()
        label.append(topic_most_pr)
        print("doc: {} topic: {}".format(n, topic_most_pr))

    # 输出主题中的TopN关键词
    word = vectorizer.get_feature_names()
    # for w in word:
    #     print(w)
    #     print(topic_word[:, :3])
    n = 10
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(word)[np.argsort(topic_dist)][:-(n + 1):-1]
        print(u'*Topic {}\n- {}'.format(i, ' '.join(topic_words)))

    # 计算文档主题分布图
    f, ax = plt.subplots(6, 1, figsize=(8, 8), sharex=True)
    for i, k in enumerate([0, 1, 2, 3, 8, 9]):
        ax[i].stem(doc_topic[k, :], linefmt='r-',
                   markerfmt='ro', basefmt='w-')
        ax[i].set_xlim(-1, 2)  # x坐标下标
        ax[i].set_ylim(0, 1.2)  # y坐标下标
        ax[i].set_ylabel("Prob")
        ax[i].set_title("Document {}".format(k))
    ax[5].set_xlabel("Topic")
    plt.tight_layout()
    # plt.show()

