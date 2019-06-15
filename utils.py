
from string import punctuation
import re
import nltk


punc = punctuation + u'.,;《》？！“”‘’@#￥%…&×（）——+【】{};；●，。&～、|\s:：'

"""
    加载文件
"""
def load_file(path):
    datas = []
    for data in open(path,encoding="utf-8"):
        datas.append(data)
    return datas

'''
    删除标点符号
'''
def delete_punctuation(fr):
    datas = []
    # 利用正则表达式替换为一个空格
    for line in fr:
        line = re.sub(r"[{}]+".format(punc)," ",line)
        datas.append(line + "\n")
    return datas

"""
    写入文件
"""
def save_file(datas, fileName):
    f = open(fileName,"w",encoding="utf-8")
    for data in datas:
        f.write(data)

"""
    @datas 数据集合
    @size 比例
    @name 存储名称

"""
def divide_data_set(datas,size,name):
    index = len(datas) * size
    save_file(datas[0:int(index)],name + "_train.txt")
    save_file(datas[int(index):],name + "_valid.txt")



"""
    @x_trian 训练数据
    @x_label 训练标签
    @y_trian 测试数据
    @y_label 测试标签
"""
def create_data(x_train,x_label,y_train,y_label):
    i = 0
    j = 0
    x_train_end = []
    x_label_end = []
    y_train_end = []
    y_label_end = []
    for data in x_train:
        if int(x_label[i]) > 10:
            x_train_end.append(data)
            x_label_end.append(int(x_label[i])-1)
        i+=1
    for data in y_train:
        if int(y_label[j]) > 10:
            y_train_end.append(data)
            y_label_end.append(int(y_label[j])-1)   
        j+=1
    return x_train_end,x_label_end,y_train_end,y_label_end

