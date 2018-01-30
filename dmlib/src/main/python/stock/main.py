# coding=utf-8
import os
import numpy as np
from src.main.python.stock import ioop
from src.main.python.stock.StockData import StockData
from src.main.python.stock.TensorflowLstm import TensorflowLstm

os.chdir("/home/nyh/work/workspace/dataanalysis/dmlib/")
np.seterr(divide='ignore')

T = 1

trainfilepath = 'data/stock/000977.SZ.train.csv'
traindata = StockData(data=ioop.get_train_data(trainfilepath=trainfilepath))
model = TensorflowLstm()
model.fit(iteration=3, traindata=traindata)

testfilepath = 'data/stock/000977.SZ.test.csv'
testdata = StockData(data=ioop.get_test_data(testfilepath=testfilepath), isTest=True)
test_true, test_predict, acc = model.predict(testdata=testdata)
model.plot(test_predict, test_true)