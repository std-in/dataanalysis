# coding=utf-8
import os
import numpy as np

from src.main.python.stock import ioop
from src.main.python.stock.StockData import StockData
from src.main.python.stock.TensorflowLstm import TensorflowLstm

os.chdir("/home/nyh/work/workspace/dataanalysis/dmlib/")
np.seterr(divide='ignore')

trainfilepath = 'data/stock/000977.SZ.train.csv'
testfilepath = 'data/stock/000977.SZ.test.csv'

data=ioop.get_train_data(trainfilepath=trainfilepath)
traindata = StockData(data=data)
testdata = StockData(data=ioop.get_test_data(testfilepath=testfilepath))

model = TensorflowLstm().fit(traindata=traindata)


# ============train============
    # lstmstock.train_lstm(iter=1000)
    #
    # ============predict===========
    # lstmstock.predictionDays()

    # test_x = lstmstock.data[len(lstmstock.data) - lstmstock.time_step:len(lstmstock.data)]
    # lstmstock.predictionDay(test_x = test_x)
    # print("true = " + str(lstmstock.data[train_end + 2][lstmstock.ylabel]))
