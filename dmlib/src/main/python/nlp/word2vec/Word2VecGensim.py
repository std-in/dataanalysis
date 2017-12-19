# -*- coding: utf-8 -*-

"""
功能：测试gensim使用，处理中文语料
时间：2016年5月21日 20:49:07
"""
from gensim.models import word2vec
import logging
import os


os.chdir("/home/nyh/work/workspace/dataanalysis/dmlib/")

# 主程序
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.PathLineSentences(u"data/nlp/stock/original/")  # 加载语料
model = word2vec.Word2Vec(sentences, size=200)  # 默认window=5

print(model.sample)
# # 计算两个词的相似度/相关程度
# print(u"【买】和【卖】的相似度为：", model.similarity(u"买", u"卖"))
# print(u"【买】和【跌】的相似度为：", model.similarity(u"买", u"下跌"))
# print(u"【卖】和【跌】的相似度为：", model.similarity(u"卖", u"下跌"))
# print("--------\n")
#
# # 计算某个词的相关词列表
# y2 = model.most_similar(u"买", topn=20)  # 20个最相关的
# print(u"和【买】最相关的词有：\n")
# for item in y2:
#     print(item[0], item[1])
# print("--------\n")
#
# # 寻找对应关系
# print(u"买入-涨停，割肉-")
# y3 = model.most_similar([u'买入', u'涨停'], [u'割肉'], topn=3)
# for item in y3:
#     print(item[0], item[1])
# print("--------\n")
#
# # 寻找不合群的词
# y4 = model.doesnt_match(u"周线 五 连阳 上面 的 套牢 盘不重 一个 板 就 上去 了 你 还 真的 是 舍得 啊 你".split())
# print(u"不合群的词：", y4)
# print("--------\n")

# 保存模型，以便重用
#model.save(u"news.model")
# 对应的加载方式
# model_2 = word2vec.Word2Vec.load("text8.model")

# 以一种C语言可以解析的形式存储词向量
#model.wv.save_word2vec_format(u"news.model.bin", binary=True)
# 对应的加载方式
# model_3 = word2vec.Word2Vec.load_word2vec_format("text8.model.bin", binary=True)
