# coding=gbk
'''
Created on 2018年1月23日
@author: ningyongheng
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os

np.seterr(divide='ignore', invalid='ignore')


class StockLstm():
    # stock name
    name = object
    # stock code
    code = object
    # stock code
    data = object

    # ——————————————————定义神经网络变量——————————————————
    # 定义常量
    # hidden layer units
    rnn_unit = 10
    input_size = 6
    output_size = 1
    lr = 0.0006  # 学习率
    # 输入层、输出层权重、偏置
    weights = {
        # tf.Variable定义tensorflow图中的变量.
        # tf.random_normal(shape,mean=0.0,stddev=1.0,dtype=tf.float32,seed=None,name=None)
        # tf.truncated_normal(shape, mean=0.0, stddev=1.0, dtype=tf.float32, seed=None, name=None)
        # tf.random_uniform(shape,minval=0,maxval=None,dtype=tf.float32,seed=None,name=None)
        # 这几个都是用于生成随机数tensor的。尺寸是shape
        # random_normal: 正太分布随机数，均值mean,标准差stddev
        # truncated_normal:截断正态分布随机数，均值mean,标准差stddev,不过只保留[mean-2*stddev,mean+2*stddev]范围内的随机数
        # random_uniform:均匀分布随机数，范围为[minval,maxval]
        'in': tf.Variable(tf.random_normal([input_size, rnn_unit])),
        'out': tf.Variable(tf.random_normal([rnn_unit, 1]))
    }
    biases = {
        # tf.constant(value,dtype=None,shape=None,name=’Const’)
        # 创建一个常量tensor，按照给出value来赋值，可以用shape来指定其形状。value可以是一个数，也可以是一个list。
        # 如果是一个数，那么这个常亮中所有值的按该数来赋值。 如果是list,那么len(value)一定要小于等于shape展开后的长度。
        # 赋值时，先将value中的值逐个存入。不够的部分，则全部存入value的最后一个值。
        'in': tf.Variable(tf.constant(0.1, shape=[rnn_unit, ])),
        'out': tf.Variable(tf.constant(0.1, shape=[1, ]))
    }

    batch_size = int
    time_step = int
    train_begin = int
    train_end = int
    ylabel = int
    test_begin = int

    def __init__(self, batch_size = 20, time_step = 15,
                 train_begin = 1, train_end = 40000,
                 ylabel = 4, test_begin = 401):
        self.batch_size = batch_size
        self.time_step = time_step
        self.train_begin = train_begin
        self.train_end = train_end
        self.iter = iter
        self.ylabel = ylabel
        self.test_begin = test_begin

    def get_all_data(self, filepath, feturebeginindex, fetureendindex):
        # ——————————————————导入数据——————————————————————
        f = open(filepath)
        df = pd.read_csv(f)  # 读入股票数据
        self.data = df.iloc[:, feturebeginindex:fetureendindex].values  # 取第1-6列

    # 获取训练集
    def get_train_data(self, input_size, batch_size, time_step, train_begin, train_end, ylabel):
        batch_index = []
        data_train = self.data[train_begin:train_end]
        # numpy.mean(a, axis=None, dtype=None, out=None, keepdims=<class numpy._globals._NoValue at 0x40b6a26c>)[source]
        # Compute the arithmetic mean along the specified axis.
        # 经常操作的参数为axis，以m * n矩阵举例：axis 不设置值，对 m*n 个数求均值，返回一个实数
        # axis = 0：压缩行，对各列求均值，返回 1* n 矩阵axis =1 ：压缩列，对各行求均值，返回 m *1 矩阵
        # np.std求标准差
        normalized_train_data = (data_train - np.mean(data_train, axis=0)) / np.std(data_train, axis=0)  # 标准化
        # normalized_train_data = data_train
        train_x, train_y = [], []  # 训练集
        for i in range(len(normalized_train_data) - time_step):
            if i % batch_size == 0:
                batch_index.append(i)
            x = normalized_train_data[i:i + time_step, :input_size]
            y = normalized_train_data[i + 1:i + time_step + 1, ylabel, np.newaxis]
            train_x.append(x.tolist())
            train_y.append(y.tolist())
        batch_index.append((len(normalized_train_data) - time_step))
        return batch_index, train_x, train_y

    # 获取测试集
    def get_test_data(self, input_size, time_step, test_begin, ylabel):
        data_test = self.data[test_begin:]
        mean = np.mean(data_test, axis=0)
        std = np.std(data_test, axis=0)
        normalized_test_data = (data_test - mean) / std  # 标准化
        # normalized_test_data = data_test
        size = (len(normalized_test_data) + time_step - 1) // time_step  # 有size个sample
        test_x, test_y = [], []
        for i in range(len(normalized_test_data) - time_step - 1):
            # x = normalized_test_data[i * time_step:(i + 1) * time_step, :input_size]
            # y = normalized_test_data[i * time_step + 1:(i + 1) * time_step + 1, ylabel]
            # test_x.append(x.tolist())
            # test_y.append(y.tolist)
            x = normalized_test_data[i:i + time_step, :input_size]
            y = normalized_test_data[i + 1:i + time_step + 1, ylabel, np.newaxis]
            test_x.append(x.tolist())
            test_y.append(y.tolist())
        # test_x.append((normalized_test_data[len(data_test) // time_step * time_step:len(data_test) - 2, :input_size]).tolist())
        # test_y.extend((normalized_test_data[len(data_test) // time_step + 1:, ylabel]).tolist())
        return mean, std, test_x, test_y

    # ——————————————————定义神经网络变量——————————————————
    def lstm(self, X):
        batch_size = tf.shape(X)[0]
        time_step = tf.shape(X)[1]
        w_in = self.weights['in']
        b_in = self.biases['in']
        # 需要将tensor转成2维进行计算，计算后的结果作为隐藏层的输入
        input = tf.reshape(X, [-1, self.input_size])
        input_rnn = tf.matmul(input, w_in) + b_in
        # 将tensor转成3维，作为lstm cell的输入
        input_rnn = tf.reshape(input_rnn, [-1, time_step, self.rnn_unit])
        with tf.variable_scope('cell_def', reuse=tf.AUTO_REUSE):
            cell = tf.nn.rnn_cell.BasicLSTMCell(self.rnn_unit)
        init_state = cell.zero_state(batch_size, dtype=tf.float32)
        with tf.variable_scope('rnn_def', reuse=tf.AUTO_REUSE):
            # output_rnn是记录lstm每个输出节点的结果，final_states是最后一个cell的结果
            output_rnn, final_states = tf.nn.dynamic_rnn(cell, input_rnn,
                                                         initial_state=init_state,
                                                         dtype=tf.float32)
        output = tf.reshape(output_rnn, [-1, self.rnn_unit])  # 作为输出层的输入
        w_out = self.weights['out']
        b_out = self.biases['out']
        pred = tf.matmul(output, w_out) + b_out
        return pred, final_states

    # ——————————————————训练模型——————————————————
    def train_lstm(self, iter = 3):
        # tf.placeholder(dtype, shape=None, name=None) 此函数可以理解为形参，用于定义过程，在执行的时候再赋具体的值
        # 参数：dtype：数据类型。常用的是tf.float32,tf.float64等数值类型
        # shape：数据形状。默认是None，就是一维值，也可以是多维，比如[2,3], [None, 3]表示列是3，行不定
        # name：名称。
        X = tf.placeholder(tf.float32, shape=[None, self.time_step, self.input_size])
        Y = tf.placeholder(tf.float32, shape=[None, self.time_step, self.output_size])
        batch_index, train_x, train_y = self.get_train_data(self.input_size, self.batch_size,
                                                            self.time_step, self.train_begin,
                                                            self.train_end, self.ylabel)
        pred, _ = self.lstm(X)
        # 损失函数
        loss = tf.reduce_mean(tf.square(tf.reshape(pred, [-1]) - tf.reshape(Y, [-1])))
        train_op = tf.train.AdamOptimizer(self.lr).minimize(loss)
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=15)
        module_file = tf.train.latest_checkpoint('model')
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            # saver.restore(sess, module_file)
            # 重复训练
            for i in range(1, iter + 2):
                for step in range(len(batch_index) - 1):
                    _, loss_ = sess.run([train_op, loss],
                                        feed_dict={X: train_x[batch_index[step]:batch_index[step + 1]],
                                                   Y: train_y[batch_index[step]:batch_index[step + 1]]})
                    # print(i, loss_)
                if i % (iter //2) == 0:
                    print("保存模型：", saver.save(sess, 'model/stock2.model', global_step=i))

    # ————————————————预测模型————————————————————
    def predictionDays(self):
        X = tf.placeholder(tf.float32, shape=[None, self.time_step, self.input_size])
        # Y=tf.placeholder(tf.float32, shape=[None,time_step,output_size])
        mean, std, test_x, test_y = self.get_test_data(self.input_size, self.time_step, self.test_begin, self.ylabel)
        pred, _ = self.lstm(X)
        saver = tf.train.Saver(tf.global_variables())
        with tf.Session() as sess:
            # 参数恢复
            module_file = tf.train.latest_checkpoint('model')
            saver.restore(sess, module_file)
            test_predict = []
            test_true = []
            for step in range(len(test_x) - 1):
                prob = sess.run(pred, feed_dict={X: [test_x[step]]})[0]
                predict = prob.reshape((-1))
                test_predict.extend(predict)
                test_true.extend(test_y[step][0])
            # 预测最后time_step个
            prob = sess.run(pred, feed_dict={X: [test_x[len(test_x) - 1]]})
            predict = prob.reshape((-1))
            test_predict.extend(predict)
            for i in range(self.time_step):
                test_true.extend(test_y[len(test_y) - 1][i])

            test_true = np.array(test_true) * float(std[self.ylabel]) + mean[self.ylabel]
            test_predict = np.array(test_predict) * std[self.ylabel] + mean[self.ylabel]
            acc = np.average(np.abs(test_predict - test_true[:len(test_predict)])
                             / test_true[:len(test_predict)])  # 偏差
            # 以折线图表示结果
            plt.figure()
            plt.plot(list(range(len(test_predict))), test_predict, color='b')
            plt.plot(list(range(len(test_true))), test_true, color='r')
            plt.show()

    # ————————————————预测模型————————————————————
    def predictionDay(self, test_x):
        X = tf.placeholder(tf.float32, shape=[None, self.time_step, self.input_size])
        mean = np.mean(test_x, axis=0)
        std = np.std(test_x, axis=0)
        normalized_test_data = (test_x - mean) / std  # 标准化
        pred, _ = self.lstm(X)
        saver = tf.train.Saver(tf.global_variables())
        with tf.Session() as sess:
            # 参数恢复
            module_file = tf.train.latest_checkpoint('model')
            saver.restore(sess, module_file)
            prob = sess.run(pred, feed_dict={X: [normalized_test_data]})
            predict = prob.reshape((-1))
            print("predict :  " + str(predict[self.time_step - 1]
                                   * std[self.ylabel] + mean[self.ylabel]))


if __name__ == '__main__':
    os.chdir("/home/nyh/work/workspace/dataanalysis/dmlib/")
    np.seterr(divide='ignore')

    ylabel = 1
    lstmstock = StockLstm(ylabel = ylabel)
    filepath = 'data/stock/000977.SZ.csv'
    feturebeginindex = 2
    fetureendindex = 7
    lstmstock.get_all_data(filepath, feturebeginindex, fetureendindex)
    train_end = 496

    # ============train============
    lstmstock.train_lstm(iter=10000)

    # ============predict===========
    # lstmstock.predictionDays()
    #
    test_x = lstmstock.data[len(lstmstock.data) - lstmstock.time_step:len(lstmstock.data)]
    lstmstock.predictionDay(test_x = test_x)
    # print("true = " + str(lstmstock.data[train_end + 2][lstmstock.ylabel]))