import string
import nltk
from gensim import corpora


def PreprocessText(text, StopWordList):
    """
    预处理一篇文本：剔除标点符号，词干化，去停用词
    :param text: 传入的文本，类型为字符串
    :param StopWordList: 停用词表
    """
    WordList = DelPunctuation(text)
    StemmeredWordList = Stemmer(WordList)
    FilteredWordList = FilterStopWords(StemmeredWordList, StopWordList)
    return FilteredWordList


def DelPunctuation(text):
    """
    剔除文本中的标点符号
    :param text:需要剔除标点符号的文本，类型为字符串
    return:返回文本中的词的序列
    """
    # delset = string.punctuation
    # 将标点符号转换为空格
    # newText = text.translate(None, delset)
    #文本中的词的列表
    WordList = [word for word in text.split(" ") if word != '' and word != ' ']
    return WordList

def FilterStopWords(WordList, StopWordList):
    """
    返回去停用词后的词表
    :param WordList:
    :param StopWordList:
    """
    FilteredWordList = filter(lambda x: x.lower() not in StopWordList, WordList)
    return FilteredWordList


def Stemmer(WordList):
    """
    对文档的词表进行词干化
    :param WordList:
    """
    stemmer = nltk.LancasterStemmer()
    StemmeredWordList = [stemmer.stem(w) for w in WordList]
    return StemmeredWordList


def ConstructDictionary(WordListSet):
    """
    根据输入文档集texts构造词典
    :rtype : object
    :param WordListSet: 文档集对应的词表，WordListSet[i]表示第i篇文档中的词
    """
    print("Begin to construct the dictionary")
    res = corpora.Dictionary(WordListSet)
    print("Total number of words is: ", len(res))
    return res


def Word2Id(WordList, Dictionary):
    """
    将词表转换为词典dictionary中的ID
    :param WordList:
    """
    IDList = []
    for word in WordList:
        #遍历字典查找目标项
        for k, v in Dictionary.items():
            if v == word:
                IDList.append(k)
    return IDList