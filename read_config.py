#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by GJT
# file 创建数据字典

import os
import json





class ReadConfig():

    def __init__(self,type):
        # 设置读取数据集的类型
        self.type = type
        self.json_str = ""
        self.__load_file()
    
    """ load config files """
    def __load_file(self):
        # 设置文件路径
        path = "config.json"
        f = open(path, "r", encoding="utf-8")
        res = f.read()
        self.json_str = json.loads(res)
        # print(self.json_str)


    def read_file(self):
        if self.type == 'train':
            return str(self.json_str['trainData'])
        elif self.type == 'test':
            return str(self.json_str['testData'])


# 文件读取测试例子
# res = ReadConfig("train").read_file()
# print(res)

# res = ReadConfig("test").read_file()
# print(res)


    