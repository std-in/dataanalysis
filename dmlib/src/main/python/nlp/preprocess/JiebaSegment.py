# coding=utf-8
import jieba
import re
import os

"""
分词 去停用词后保存文件
"""


def getWords(inputPath, outputPath):
    stopWords = []
    for line in open("data/nlp/stopWords.txt").readlines():
        stopWords.append(line.strip())
    for file in os.listdir(inputPath):
        fw = open(outputPath + '/' + file + ".txt", 'w+')
        for line in open(inputPath + '/' + file).readlines():
            newline = ' '.join(word for word in jieba.cut(''.join(
                re.findall(u'[\u4e00-\u9fff]+', line))) if word not in stopWords)
            fw.write(newline)
        fw.close()


if __name__ == '__main__':
    os.chdir("/home/nyh/work/workspace/dataanalysis/dmlib/")
    getWords("data/nlp/stock/original", 'data/output')