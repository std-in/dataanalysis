#-*- coding: utf-8 -*-
# from http://kexue.fm/archives/3360/
import numpy as np #导入numpy
import pandas as pd
import jieba
import os

def yuchuli(s,m): #导入文本，文本预处理
    wenjian = pd.read_csv(s, delimiter='     xxx     ', encoding='utf-8', \
                          header= None, names=['comment']) #导入文本
    wenjian = wenjian['comment'].str.replace('(<.*?>.*?<.*?>)','').str.replace('(<.*?>)','') \
        .str.replace('(@.*?[ :])',' ') #替换无用字符
    wenjian = pd.DataFrame({'comment':wenjian[wenjian != '' ]})
    # wenjian.to_csv('out_'+s, header=False, index=False)
    wenjian.to_csv(s, header=False, index=False)
    wenjian['mark'] = m #样本标记
    return wenjian.reset_index()

print(os.getcwd())
print(os.path.abspath("../../../../../data/data_neg.txt"))
neg = yuchuli('../../../../../data/sentiment/data_neg.txt', -1)
pos = yuchuli('../../../../../data/sentiment/data_pos.txt', 1)

mydata = pd.concat([neg,pos],ignore_index=True)[['comment','mark']] #结果文件
#预处理基本结束

#开始加载情感词典
negdict = [] #消极情感词典
posdict = [] #积极情感词典
nodict = [] #否定词词典
plusdict = [] #程度副词词典
sl = pd.read_csv('dict/neg.txt', header=None, encoding='utf-8')
for i in range(len(sl[0])):
    negdict.append(sl[0][i])
sl = pd.read_csv('dict/pos.txt', header=None, encoding='utf-8')
for i in range(len(sl[0])):
    posdict.append(sl[0][i])
sl = pd.read_csv('dict/no.txt', header=None, encoding='utf-8')
for i in range(len(sl[0])):
    nodict.append(sl[0][i])
sl = pd.read_csv('dict/plus.txt', header=None, encoding='utf-8')
for i in range(len(sl[0])):
    plusdict.append(sl[0][i])
#加载情感词典结束
#预测函数
def predict(s, negdict, posdict, nodict, plusdict):
    p = 0
    sd = list(jieba.cut(s))
    for i in range(len(sd)):
        if sd[i] in negdict:
            if i>0 and sd[i-1] in nodict:
                p = p + 1
            elif i>0 and sd[i-1] in plusdict:
                p = p - 2
            else: p = p - 1
        elif sd[i] in posdict:
            if i>0 and sd[i-1] in nodict:
                p = p - 1
            elif i>0 and sd[i-1] in plusdict:
                p = p + 2
            elif i>0 and sd[i-1] in negdict:
                p = p - 1
            elif i<len(sd)-1 and sd[i+1] in negdict:
                p = p - 1
            else: p = p + 1
        elif sd[i] in nodict:
            p = p - 0.5
    return p
#预测函数结束
#简单的测试
tol = 0
yes = 0
mydata['result'] = 0
for i in range(len(mydata)):
    print(i)
    tol = tol + 1
    if predict(mydata.loc[i,'comment'], negdict, posdict, nodict, plusdict)*mydata.loc[i,'mark'] > 0:
        yes = yes + 1
        mydata.loc[i,'result'] = 1

print(yes/tol)