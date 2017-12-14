import ListUtil
import os
import LoadData
import Preprocess


class LDAModel:
    alpha = float  # 超参数alpha
    beta = float  # 超参数beta
    D = int  # 文档数目
    K = int  # 主题个数
    W = int  # 词的个数
    NumberOfIterations = int  # 迭代次数
    SaveStep = int  # 存储的步数

    Dictionary = object  # 整个语料的词典
    Z = object  # D * doc.size()大小的矩阵，Z[i][j]表示第i文档的第j个词背分配的主题
    W = object  # D * doc.size()大小的矩阵， W[i][j]表示第i文档的第j个词
    IDListSet = object  # D * doc.size()大小的矩阵， IDListSet[i][j]表示第i篇文档的第j个词在词典中的编号
    nw = object  # W * K 大小的矩阵， nw[w][z]表示词w被分配到主题z的次数
    nd = object  # D * K 大小的矩阵，nd[d][z]文档d中被分配为主题z的词的个数
    nwsum = object  # K * 1 大小的向量，nwsum[z]表示主题z中包含的词的个数
    ndsum = object  # D * 1 大小的向量，ndsum[d]表示文档d中包含的词的个数
    theta = object  # D * K 大小的矩阵，p(z|d) = theta[d][z]
    phi = object  # K * V 大小的矩阵，p(w|z) = phi[z][w]

    # 构造函数，alpha一般取50/K, beta一般取0.01,吉布斯抽样的迭代次数一般为1000次
    def __init__(self, alpha, beta, NumberOfIterations, SaveStep, K):
        self.alpha = alpha
        self.beta = beta
        self.NumberOfIterations = NumberOfIterations
        self.SaveStep = SaveStep
        self.K = K
        # 初始化大小为K * 1的向量，初始值为0
        self.nwsum = ListUtil.Initial(self.K)

    def ModelInit(self, filename):
        """
        读取文档，文本预处理，构造词典，构造语料库
        """
        Docs = LoadData.LoadDataFromFile(filename)
        self.D = len(Docs)
        print("Load ", self.D, " docs from the file")
        # 读取停用词表
        StopWordList = LoadData.LoadStopWords()
        # 对输入文本进行预处理：去标点符号，去停用词，词干化，然后每篇文档生成一个词的列表
        WordListSet = [Preprocess.PreprocessText(doc, StopWordList) for doc in Docs]
        # 通过词表集构造词典
        self.Dictionary = Preprocess.ConstructDictionary(WordListSet)
        self.W = len(self.Dictionary)
        # print("Total number of words is: ", self.W)
        # print("Begin to save the dictionary...")
        # self.SaveDictionary()
        # print("Done!!")
        # IDListSet 大小 D * doc.size()
        print("Begin to map the word to ID")
        self.IDListSet = []
        for wdl in WordListSet:
            IdList = Preprocess.Word2Id(wdl, self.Dictionary)
            self.IDListSet.append(IdList)
        print("Done!!")
        # ndsum[d] 文档d中包含的词的个数
        self.ndsum = ListUtil.Initial(self.D)
        # 初始化一个 D * K的矩阵
        self.theta = ListUtil.InitialMat(self.D, self.K, 0.0)
        self.phi = ListUtil.InitialMat(self.K, self.W, 0.0)
        # nd[d][z] 文档d中被分配给主题z的词数
        self.nd = ListUtil.InitialMat(self.D, self.K, 0)
        # nw[w][z] 主题z中包含的词w的个数
        self.nw = ListUtil.InitialMat(self.W, self.K, 0)
        # Z[d][w] 文档d的第w个词的主题
        self.Z = []
        print("Begin to initialize the LDA model...")
        # 初始化计数向量和计数矩阵
        self.RandomAssignTopic()
        print("Topic assignment done!!")

    def RandomAssignTopic(self):
        """
        随机为文档中的词分配主题
        更新计数向量ndsum, nwsum, 计数矩阵nd, nw的值
        """
        for d in range(self.D):
            DocSize = len(self.IDListSet[d])
            row = ListUtil.Initial(DocSize)
            self.Z.append(row)
            for w in range(DocSize):
                # 从主题编号0-K-1中随机抽取一个
                topic = Sample.UniSample(self.K)
                # 获取词的ID
                wid = self.IDListSet[d][w]
                self.Z[d][w] = topic
                # 被分派给topic的词w的数目自增1
                self.nw[wid][topic] += 1
                # 文档d中被分配给主题topic的词的个数
                self.nd[d][topic] += 1
                # 主题topic中包含的总的词数
                self.nwsum[topic] += 1
            self.ndsum[d] = DocSize

    def sampling(self, d, w):
        """
        Gibbs Sampling为当前词重新分配主题
        :param d: 文档编号
        :param w: 词在文档中的编号
        """
        topic = self.Z[d][w]
        # 对应位置上的词的ID
        wid = self.IDListSet[d][w]
        self.nw[wid][topic] -= 1
        self.nd[d][topic] -= 1
        self.nwsum[topic] -= 1
        self.ndsum[d] -= 1

        # p为马尔可夫链传递概率，p[z]表示当前词被分配到主题z的概率
        p = self.ComputeTransProb(d, w)

        # 从多项分布中抽取新的主题
        newtopic = Sample.MultSample(p)
        self.nw[wid][newtopic] += 1
        self.nd[d][newtopic] += 1
        self.nwsum[newtopic] += 1
        self.ndsum[d] += 1
        return newtopic

    def ComputeTransProb(self, d, w):
        """
        对第d篇文档的第w个词
        计算Gibbs Sampling过程中的传递概率
        :param d: 文档编号
        :param w: 词在文档中的编号
        """
        # 用于平滑
        Wbeta = self.W * self.beta
        Kalpha = self.K * self.alpha
        # 第d篇文档，第w个词对应的id
        wid = self.IDListSet[d][w]
        p = ListUtil.Initial(self.K, 0.0)
        for k in range(self.K):
            # p[k] = p(w|k)*p(k|d)   k为主题
            p[k] = (float(self.nw[wid][k]) + self.beta) / (float(self.nwsum[k]) + Wbeta) * (
            float(self.nd[d][k]) + self.alpha) / (float(self.ndsum[d]) + Kalpha)
        return p

    def UniSample(K):
        """
        产生从O到K－1的整数
        :param K: 主题个数
        """
        return RandomNumber.RandInt(0, K - 1)

    def MultSample(ProbList):
        """
        从多项分布ProbList中采样, ProbList表示剔除当前词之后的主题分布
        :param ProbList: 多项分布
        """
        size = len(ProbList)
        for i in range(1, size):
            ProbList[i] += ProbList[i - 1]
            # 随机产生一个［0，1）的小数
            u = RandomNumber.RandFloat()
        res = 0
        for k in range(size):
            if ProbList[k] >= u * ProbList[size - 1]:
                # 抽样结果
                res = k
                break
        # res为抽样后的主题编号
        return res

    def ComputTheta(self):
        """
        计算p(z|d)矩阵
        size:D * K
        p(z|d) = theta[d][z]
        """
        for d in range(self.D):
            for k in range(self.K):
                self.theta[d][k] = (float(self.nd[d][k]) + self.alpha) \
                                   / (float(self.ndsum[d]) + self.K * self.alpha)

    def ComputePhi(self):
        """
        计算p(w|z)
        size:K * W
        p(w|z) = phi[z][w]
        """
        for k in range(self.K):
            for w in range(self.W):
                self.phi[k][w] = (self.nw[w][k] + self.beta) \
                                 / (self.nwsum[k] + self.W * self.beta)

    def estimate(self):
        """
        LDA参数估计
        """
        for i in range(1, self.NumberOfIterations + 1):
            for d in range(self.D):
                for w in range(len(self.IDListSet[d])):
                    newtopic = self.sampling(d, w)
                    # 为当前词分派新主题
                    self.Z[d][w] = newtopic
            if i % self.SaveStep == 0:
                # 计算当前的迭代结果
                self.ComputTheta()
                self.ComputePhi()
                # self.SaveTempRes(i)


if __name__ == '__main__':
    lda = LDAModel(25, 0.01, 500, 50, 2)
    lda.ModelInit('/home/nyh/work/workspace/dataanalysis/dmlib/data/news/sport')
    # lda.ModelInit('/home/nyh/work/workspace/dataanalysis/dmlib/data/nlp/stock/original/000889comments')
    lda.estimate()
    print(lda.theta)
