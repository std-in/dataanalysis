# coding=utf-8
import pandas as pd


def get_all_data(self, filepath, feturebeginindex, fetureendindex):
    # ——————————————————导入数据——————————————————————
    f = open(filepath)
    df = pd.read_csv(f)  # 读入股票数据
    data = df.iloc[:, feturebeginindex:fetureendindex].values  # 取第1-6列


def get_train_data(trainfilepath):
    f = open(trainfilepath)
    # 读入股票数据
    return pd.read_csv(f)


def get_test_data(testfilepath):
    f = open(testfilepath)
    return pd.read_csv(f)
