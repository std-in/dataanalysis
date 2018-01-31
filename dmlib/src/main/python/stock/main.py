# coding=utf-8
import os
import numpy as np
from src.main.python.stock import ioop
from src.main.python.stock.StockData import StockData
from src.main.python.stock.TensorflowLstm import TensorflowLstm

os.chdir("/home/nyh/work/workspace/dataanalysis/dmlib/")
np.seterr(divide='ignore')

T = 2
time_step = 20

model = TensorflowLstm()
trainfilepath = 'data/stock/000977.SZ.train.csv'
traindata = StockData(data=ioop.get_train_data(trainfilepath=trainfilepath),
                      time_step=time_step, normalize=False, isPercent=True, T=T)
model.fit(iteration=1000, traindata=traindata)

testfilepath = 'data/stock/000977.SZ.test.csv'
testdata = StockData(data=ioop.get_test_data(testfilepath=testfilepath),
                     time_step=time_step, normalize=False, isPercent=True, isTest=True, T=T)
test_true, test_predict, acc = model.predict(testdata=testdata)
print('acc :   ' + str(acc))
model.plot(test_predict, test_true)

# T = 2 normalize=False, isPercent=True, time_step = 15
