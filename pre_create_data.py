#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by GJT


import wordninja as wdja
import pickle
import wordcheck

data_path = "data\\data_student.pkl"

root = "datasets\\"

x_train,y_train,x_valid,y_valid = pickle.load(open(data_path,'rb'))

x_train_file = open(root + "trian.txt", "w", encoding="utf-8")
x_train_list = []
# 处理训练集和
for data in x_train:
    # 拆分单词
    data = wdja.split(data)
    data1 = []
    for data2 in data:
        # 单词拼写纠正
        data1.append(wordcheck.correct(data2))
    strs = " ".join(list(data1))
    x_train_list.append(strs)
    x_train_file.write(strs + "\n")

x_valid_file = open(root + "valid.txt", "w", encoding="utf-8")
x_valid_list = []
# 处理
for data in x_valid:
    data = wdja.split(data)
    data1 = []
    for data2 in data:
        # 单词拼写纠正
        data1.append(wordcheck.correct(data2))
    strs = " ".join(data1)
    x_valid_list.append(strs)
    x_valid_file.write(strs + "\n")
