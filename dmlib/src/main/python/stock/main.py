# coding=utf-8
import os
import numpy as np
from src.main.python.stock import ioop
from src.main.python.stock.StockData import StockData
from src.main.python.stock.TensorflowLstm import TensorflowLstm
import time
import tushare as ts
import os
import tensorflow as tf

os.chdir("/home/nyh/work/workspace/dataanalysis/dmlib/")
np.seterr(divide='ignore')


def test(stockcode):
    T = 2
    time_step = 15

    inputsize = 13
    model = TensorflowLstm(input_size=inputsize)

    # date：日期 open：开盘价 high：最高价 close：收盘价 low：最低价 volume：成交量 price_change：价格变动
    # p_change：涨跌幅 ma5：5日均价 ma10：10日均价 ma20:20日均价 v_ma5:5日均量 v_ma10:10日均量 v_ma20:20日均量 turnover:换手率[注：指数无此项]
    data1 = ts.get_hist_data(stockcode, start='2010-01-05',
                             end=time.strftime('%Y-%m-%d', time.localtime(time.time())))
    traindata = StockData(data=data1,
                          featureend=(inputsize + 1),
                          time_step=time_step, normalize=True, needPercent=False, T=T)
    model.fit(iteration=5, traindata=traindata)

    data2 = ts.get_hist_data('000977', start='2017-10-09', end='2018-2-1')
    testdata = StockData(data=data2,
                         featureend=(inputsize + 1),
                         time_step=time_step, normalize=True, needPercent=False, isTest=True, T=T)
    test_true, test_predict, acc = model.predict(testdata=testdata)

    print('acc :   ' + str(acc))
    for i in range(T):
        change = (test_predict[len(test_predict) - (T - i)] - test_true[len(test_true) - 1]) / test_true[len(test_true) - 1]
        print(stockcode + ' | T = ' + str(i + 1) + ' | 涨跌幅:  | ' + str(change * 100)
              + " | 预测价格 : | " + str(test_predict[len(test_predict) - (T - i)]))

    model.plot(test_predict, test_true)
    # T = 2 normalize=False, isPercent=True, time_step = 15


def scan(stockcode, T=2):
    time_step = 30

    inputsize = 11
    model = TensorflowLstm(input_size=inputsize)

    # date：日期 open：开盘价 high：最高价 close：收盘价 low：最低价 volume：成交量 price_change：价格变动
    # p_change：涨跌幅 ma5：5日均价 ma10：10日均价 ma20:20日均价 v_ma5:5日均量 v_ma10:10日均量 v_ma20:20日均量 turnover:换手率[注：指数无此项]
    data1 = ts.get_hist_data(stockcode, start='2010-01-05',
                             end=time.strftime('%Y-%m-%d', time.localtime(time.time())))
    traindata = StockData(code=stockcode, data=data1,
                          featureend=inputsize,
                          time_step=time_step, normalize=True, needPercent=True, T=T)
    model.fit(iteration=10, traindata=traindata)

    data2 = ts.get_hist_data(stockcode, start='2017-10-8',
                             end=time.strftime('%Y-%m-%d', time.localtime(time.time())))
    testdata = StockData(code=stockcode, data=data2,
                         featureend=inputsize,
                         time_step=time_step, normalize=True, needPercent=True, T=T)
    test_true, test_predict, acc, ud_test_predict, ud_test_true = model.predict(testdata=testdata)

    # print('acc :   ' + str(acc))
    f = open('out/result', 'a+')
    for i in range(T):
        change = (test_predict[len(test_predict) - (T - i)] - test_true[len(test_true) - 1]) / test_true[len(test_true) - 1]
        # print(stockcode + ' | T = ' + str(i + 1) + ' | 涨跌幅:  | ' + str(change * 100)
        #       + " | 预测价格 : | " + str(test_predict[len(test_predict) - (T - i)]))
        f.write(stockcode + ' | T = ' + str(i + 1) + ' | 涨跌幅:  | ' + str(change * 100)
                + " | 当前价格 : | " + str(test_true[len(test_true) - (T - i)])
                + " | 预测价格 : | " + str(test_predict[len(test_predict) - (T - i)]))
        f.write('\n')
    f.close()
    model.plot(testdata.time, test_predict, test_true)
    model.plot(testdata.time, ud_test_predict, ud_test_true)


    # T = 2 normalize=False, isPercent=True, time_step = 15


if __name__ == '__main__':
    stockcodes = ['300370', '300058', '300364', '300287', '300277', '300092',
                  '300136', '300251', '300661', '300107', '300462', '300271', '300582', '300253',
                  '300226', '300308', '300474', '300164', '300433', '300166', '300602', '300040',
                  '300373', '300133', '300413', '300313', '300027', '300584', '300054', '300556',
                  '300323', '300097', '300315', '300269', '300466', '300144', '300044', '300367',
                  '300044', '300358', '300212', '300385', '300003', '300301', '300316', '300320',
                  '300497', '300088', '300078', '300231', '300519', '300431', '300191', '300666',
                  '300706', '300353', '300438', '300209', '300401', '300115', '300207', '300002',
                  '300541', '300567', '300398', '300168', '300043', '300725', '300059', '300124',
                  '300046', '300239', '300123', '300663', '300613', '300222', '300053', '300017',
                  '300327', '300059', '300322', '300024', '300440', '300496', '300072', '300379',
                  '300631', '300122', '300736', '300228', '300723', '300735', '300236', '300452',
                  '300408', '300407', '300311', '300604']
    # for code in stockcodes:
    #     if not os.path.isdir('model/stock/' + code):
    #         os.mkdir('model/stock/' + code)
    #     tf.reset_default_graph()
    #     scan(code, T=1)
    #     tf.reset_default_graph()
    #     scan(code, T=2)

    # scan('000977', T=1)
    # tf.reset_default_graph()
    scan('000977', T=2)
    # tf.reset_default_graph()
    # scan('000977', T=3)