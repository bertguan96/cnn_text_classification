#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by GJT
# 准确率校验方法

import pickle
from sklearn.metrics import accuracy_score

data_path = "data\\data_student.pkl"
    
root = "datasets\\"


def get_acc():
    x_train,y_train,x_valid,y_valid = pickle.load(open(data_path,'rb')) 
    y_test = list(y_valid)
    y_predict = list()
    for y in open(root + 'result.txt','r'):
        y = str(y).strip('\n')   # 去除末尾换行符
        y_predict.append(int(y))
    print(accuracy_score(y_predict, y_test))
get_acc()