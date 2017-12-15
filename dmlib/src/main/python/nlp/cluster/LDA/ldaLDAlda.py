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


class LdaModel:
    filepath = str
    niter = int
    ntopics = int
    randomstate = 1
    corpus = object
    X = object
    model = object
    vectorizer = object

    def __init__(self, filepath, ntopics, niter):
        self.filepath = filepath
        self.ntopics = ntopics
        self.niter = niter
        self.vectorizer = CountVectorizer()

    def readCorpus(self):
        corpus = []
        if os.path.isdir(self.filepath):
            for file in os.listdir(self.filepath):
                for line in open(self.filepath + '/' + file, 'r').readlines():
                    newline = ' '.join(jieba.cut(''.join(re.findall(u'[\u4e00-\u9fff]+', line))))
                    if len(newline) > 5:
                        corpus.append(newline)
                    else:
                        pass
        else:
            for line in open(self.filepath, 'r').readlines():
                newline = ' '.join(jieba.cut(''.join(re.findall(u'[\u4e00-\u9fff]+', line))))
                if len(newline) > 5:
                    corpus.append(newline)
                else:
                    pass
        self.corpus = corpus

    def train(self):
        print('training:')
        # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
        self.X = self.vectorizer.fit_transform(self.corpus)

        # analyze = vectorizer.build_analyzer()
        # weight = self.X.toarray()
        # print(str(weight))
        # print(weight[:5, :5])

        # LDA算法
        print('LDA:')
        self.model = lda.LDA(n_topics=self.ntopics,
                             n_iter=self.niter, random_state=self.randomstate)
        # model.fit(np.asarray(weight))  
        self.model.fit_transform(self.X)

    def getInfo(self):
        print('some info as follows:')
        # model.fit(np.asarray(weight))
        topic_word = self.model.topic_word_  # model.components_ also works

        # 文档-主题（Document-Topic）分布
        doc_topic = self.model.doc_topic_
        print("type(doc_topic): {}".format(type(doc_topic)))
        print("shape: {}".format(doc_topic.shape))

        # 输出前10篇文章最可能的Topic
        label = []
        for n in range(10):
            topic_most_pr = doc_topic[n].argmax()
            label.append(topic_most_pr)
            print("doc: {} topic: {}".format(n, topic_most_pr))

        # 输出主题中的TopN关键词
        word = self.vectorizer.get_feature_names()
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
            ax[i].stem(doc_topic[k, :], linefmt='r-', markerfmt='ro', basefmt='w-')
            ax[i].set_xlim(-1, 2)  # x坐标下标
            ax[i].set_ylim(0, 1.2)  # y坐标下标
            ax[i].set_ylabel("Prob")
            ax[i].set_title("Document {}".format(k))
        ax[5].set_xlabel("Topic")
        plt.tight_layout()
        # plt.show()
        print('=' * 50)
        print("the cluster is:")
        label = []
        # 输出到文件
        file_object = open('output.txt', 'w+')
        # 按类别输出每一个文档(行)
        for n in range(self.ntopics):
            for i in range(len(self.corpus)):
                if doc_topic[i].argmax() == n:
                    file_object.write("label: {} feature: {} \n".format(n,self.corpus[i]))
        file_object.close()

if __name__ == '__main__':
    # filepath = '/home/nyh/work/workspace/dataanalysis/dmlib/data/news/'
    filepath = '/home/nyh/work/workspace/dataanalysis/dmlib/data/nlp/stock/original'
    ntopics = 2
    niter = 1000
    ldamodel = LdaModel(filepath, ntopics, niter)
    ldamodel.readCorpus()
    ldamodel.train()
    ldamodel.getInfo()
