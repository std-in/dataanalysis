import os
import string


def LoadDataFromFile(path):
    """
    :param path:短文本存放路径
    """
    #转换为绝对路径
    fp = open(path, 'r')
    Docs = []
    for line in fp:
        #去掉结尾换行符
        ll = line.strip('\n').strip('\r')
        Docs.append(ll)
    fp.close()
    print("Done, load ", len(Docs), " docs from the file")
    return Docs


def LoadStopWords():
    """
    从指定路径读取停用词表
    return:停用词列表
    """
    path = '/home/nyh/work/workspace/dataanalysis/dmlib/data/nlp/stock/StopWords.txt'
    fp = open(path, 'r')
    #获取停用词列表
    StopWordsList = [line.strip('\n') for line in fp]
    fp.close()
    return StopWordsList


def LoadDictionary():
    """
    从指定路径加载训练词典
    """
    path = os.getcwd() + "/dictionary.txt"
    fp = open(path, 'r')
    Dictionary = dict()
    for line in fp:
        elements = line.strip('\n').split(" ")
        #词的id
        k = string.atoi(elements[0])
        #词本身
        v = elements[1]
        Dictionary[k] = v
    fp.close()
    return Dictionary