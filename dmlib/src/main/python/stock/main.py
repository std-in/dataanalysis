# coding=utf-8
import os
import numpy as np
from src.main.python.stock import ioop
from src.main.python.stock.StockData import StockData
from src.main.python.stock.TensorflowLstm import TensorflowLstm
import tushare as ts

os.chdir("/home/nyh/work/workspace/dataanalysis/dmlib/")
np.seterr(divide='ignore')


def test000977():
    T = 2
    time_step = 15

    inputsize = 6
    model = TensorflowLstm(input_size=inputsize)

    trainfilepath = 'data/stock/000977.SZ.train.csv'
    traindata = StockData(data=ioop.get_train_data(trainfilepath=trainfilepath),
                          featureend=(inputsize + 1),
                          time_step=time_step, normalize=True, needPercent=True, T=T)
    model.fit(iteration=2000, traindata=traindata)

    testfilepath = 'data/stock/000977.SZ.test.csv'
    testdata = StockData(data=ioop.get_test_data(testfilepath=testfilepath),
                         featureend=(inputsize + 1),
                         time_step=time_step, normalize=True, needPercent=True, isTest=True, T=T)
    test_true, test_predict, acc = model.predict(testdata=testdata)

    print('acc :   ' + str(acc))
    for i in range(T):
        print('涨跌预测 T = ' + str(i + 1) + ':   '+ str(test_predict[len(test_predict) - (T - i)]))

    model.plot(test_predict, test_true)
    # T = 2 normalize=False, isPercent=True, time_step = 15


def test300335():
    T = 2
    time_step = 30

    inputsize = 5
    model = TensorflowLstm(input_size=inputsize)

    trainfilepath = 'data/stock/300335.SZ.train.csv'
    traindata = StockData(data=ioop.get_train_data(trainfilepath=trainfilepath),
                          featureend=(inputsize + 1),
                          time_step=time_step, normalize=True, isPercent=True, T=T)
    model.fit(iteration=2000, traindata=traindata)

    testfilepath = 'data/stock/300335.SZ.test.csv'
    testdata = StockData(data=ioop.get_test_data(testfilepath=testfilepath),
                         featureend=(inputsize + 1),
                         time_step=time_step, normalize=True, isPercent=True, isTest=True, T=T)
    test_true, test_predict, acc = model.predict(testdata=testdata)

    for i in range(T):
        print('涨跌预测 T = ' + str(i + 1) + ':   ' + str(test_predict[len(test_predict) - (T - i)]))

    model.plot(test_predict, test_true)


def testTu000977():
    T = 2
    time_step = 15

    inputsize = 13
    model = TensorflowLstm(input_size=inputsize)

    # date：日期 open：开盘价 high：最高价 close：收盘价 low：最低价 volume：成交量 price_change：价格变动
    # p_change：涨跌幅 ma5：5日均价 ma10：10日均价 ma20:20日均价 v_ma5:5日均量 v_ma10:10日均量 v_ma20:20日均量 turnover:换手率[注：指数无此项]
    data1 = ts.get_hist_data('000977', start='2010-01-05', end='2017-10-09')
    traindata = StockData(data=data1,
                          featureend=(inputsize + 1),
                          time_step=time_step, normalize=False, needPercent=False, T=T)
    model.fit(iteration=1000, traindata=traindata)

    data2 = ts.get_hist_data('000977', start='2017-10-09', end='2018-2-1')
    testdata = StockData(data=data2,
                         featureend=(inputsize + 1),
                         time_step=time_step, normalize=False, needPercent=False, isTest=True, T=T)
    test_true, test_predict, acc = model.predict(testdata=testdata)

    print('acc :   ' + str(acc))
    for i in range(T):
        print('涨跌预测 T = ' + str(i + 1) + ':   '+ str(test_predict[len(test_predict) - (T - i)]))

    model.plot(test_predict, test_true)
    # T = 2 normalize=False, isPercent=True, time_step = 15


if __name__ == '__main__':
    # test000977()
    # test300335()
    testTu000977()
