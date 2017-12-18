# coding=utf-8
import os
import jieba
import re


"""
短文本的情感识别(分类),使用词典匹配的方法 
"""


class SentimentShortText:
    nodict = dict()
    posdict = dict()
    negdict = dict()
    plusdict = dict()
    stopWords = list()

    def __init__(self, path):
        os.chdir(path)

    def readDict(self):
        for line in open("data/nlp/neg.txt", 'r').readlines():
            self.negdict[line.strip()] = -1
        for line in open("data/nlp/pos.txt", 'r').readlines():
            self.posdict[line.strip()] = 1
        for line in open("data/nlp/no.txt", 'r').readlines():
            self.nodict[line.strip()] = -1
        for line in open("data/nlp/plus.txt", 'r').readlines():
            self.plusdict[line.strip()] = 2
        for line in open("data/nlp/stopWords.txt", 'r').readlines():
            self.stopWords.append(line.strip())

    def predict(self, path):
        for line in open(path):
            words = ' '.join(jieba.cut(''.join(re.findall(u'[\u4e00-\u9fff]+', line)), cut_all = True))
            score = 1
            for word in words:
                if word in self.stopWords:
                    pass
                if word in self.negdict:
                    score *= -1
                if word in self.nodict:
                    score *= -1
                if word in self.plusdict:
                    score *= 2
            print("score: {} feature {}".format(score, line))


if __name__ == '__main__':
    sst = SentimentShortText('/home/nyh/work/workspace/dataanalysis/dmlib/')
    sst.predict("data/nlp/stock/samplecomments")