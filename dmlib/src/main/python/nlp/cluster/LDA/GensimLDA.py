import gensim
import os
import jieba
import re

filepath = "/home/nyh/work/workspace/dataanalysis/dmlib/data/news/"
text = []
fp = open('/home/nyh/work/workspace/dataanalysis/dmlib/data/nlp/stopWords.txt', 'r')
StopWordsList = [line.strip() for line in fp]
for filename in os.listdir(filepath):
    file = open(filepath + filename)
    line = file.readline()
    text.append(' '.join(jieba.cut(''.join(re.findall(u'[\u4e00-\u9fff]+', line)))))
    while line:
        line = file.readline()
        text.append(' '.join(word for word in jieba.cut(''.join(re.findall(u'[\u4e00-\u9fff]+', line))) if word not in StopWordsList))
    file.close()

words = []
for doc in text:
    tdoc = doc.split(" ")
    if len(tdoc) < 2:
        pass
    else:
        words.append(tdoc)

# obtain: (word_id:word)
word_count_dict = gensim.corpora.Dictionary(words)

# print(words)
# 自建词典
dict = gensim.corpora.Dictionary(words)

# 通过dict将用字符串表示的文档转换为用id表示的文档向量
corpus = [dict.doc2bow(text) for text in words]

# corpus = corpus = [[(0, 1.0), (1, 1.0), (2, 1.0)],
#                    [(2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (8, 1.0)],
#                    [(1, 1.0), (3, 1.0), (4, 1.0), (7, 1.0)],
#                    [(0, 1.0), (4, 2.0), (7, 1.0)],
#                    [(3, 1.0), (5, 1.0), (6, 1.0)],
#                    [(9, 1.0)],
#                    [(9, 1.0), (10, 1.0)],
#                    [(9, 1.0), (10, 1.0), (11, 1.0)],
#                    [(8, 1.0), (10, 1.0), (11, 1.0)]]

# lda_model = gensim.models.LdaModel(corpus, num_topics=2, id2word=word_count_dict, passes=5)
lda_model = gensim.models.LdaModel(corpus, num_topics=2)
# 输出主题
lda_model.print_topics(2)