# -*- coding: utf-8 -*-

"""
功能：测试gensim使用，处理中文语料
时间：2016年5月21日 20:49:07
"""
from gensim.models import word2vec
import logging

# 主程序
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.Text8Corpus(u"/home/nyh/work/workspace/dataanalysis/dmlib/data/word2vec/swresult_withoutnature.txt")  # 加载语料
model = word2vec.Word2Vec(sentences, size=200)  # 默认window=5

# 计算两个词的相似度/相关程度
y1 = model.similarity(u"无产阶级", u"社会主义")
print(u"【无产阶级】和【社会主义】的相似度为：", y1)
print("--------\n")

# 计算某个词的相关词列表
y2 = model.most_similar(u"精神", topn=20)  # 20个最相关的
print(u"和【精神】最相关的词有：\n")
for item in y2:
    print(item[0], item[1])
print("--------\n")

# 寻找对应关系
print(u"坚持-思想，发展-")
y3 = model.most_similar([u'坚持', u'思想'], [u'发展'], topn=3)
for item in y3:
    print(item[0], item[1])
print("--------\n")

# 寻找不合群的词
y4 = model.doesnt_match(u"中国 人民 党中央".split())
print(u"不合群的词：", y4)
print("--------\n")

# 保存模型，以便重用
model.save(u"news.model")
# 对应的加载方式
# model_2 = word2vec.Word2Vec.load("text8.model")

# 以一种C语言可以解析的形式存储词向量
model.wv.save_word2vec_format(u"news.model.bin", binary=True)
# 对应的加载方式
# model_3 = word2vec.Word2Vec.load_word2vec_format("text8.model.bin", binary=True)

if __name__ == "__main__":
    pass