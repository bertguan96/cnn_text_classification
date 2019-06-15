import os
import pickle
import numpy as np
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer  
import nltk

data_path = "data\\data_student.pkl"
x_train,y_train,x_valid,y_valid = pickle.load(open(data_path,'rb')) 

stop_words = set(stopwords.words('english'))
root = ""

# 分词过后的数组

# 词向量最终结果
doc_term_matrix = []

def participle_to_label(text):
    participle_arr = []
    # 词向量
    word_dict = dict()
    word_set = set()
    for doc in text:
        
        doc_arr = doc.split()
        origin_arr = []
        for doc_word in doc_arr:
            # 去停止词语
            if doc_word not in stop_words:
                # 利用porter进行词干还原
                origin_word = nltk.stem.WordNetLemmatizer().lemmatize(doc_word)
                # origin_word = porter_stemmer.stem(doc_word)
                origin_arr.append(origin_word)
        participle_arr.append(doc_arr)
    # 将结果转换为set
    for i in range(len(participle_arr)):
        word_set = word_set.union(participle_arr[i])
    # word_set = set(participle_arr[0]).union(participle_arr[1]).union(participle_arr[2])
    # 将set转换为dict
    i = 0
    word_dict = dict()
    for word in word_set:
        word_dict[word] = i
        i+=1
    return word_dict,participle_arr

"""
    将participle_arr数组中的数据转换为对应dict中的位置
"""
def tf(word_dict, participle_arr):       
    index = 0
    index_arr = []
    for participle_word in participle_arr:
        index_list = []
        for word in participle_word:
            index = word_dict[word]
            index_list.append(index)
        participle_word = []
        participle_word = index_list
        index_arr.append(participle_word)
    participle_arr = []
    participle_arr = index_arr
    return participle_arr

""" 
    @method create file list
    @param data_path the files root path
    @param text_list need to write path
    @param fileName create files name
"""
def create_train_text(data_path, text_list,fileName):
    if os.path.exists(data_path):
        files = open(data_path+fileName, "w",encoding="utf-8")
        for text in text_list:
            files.write(text + "\n")
    else:
        os.makedirs(data_path)

""" make the word to vec """
def read_file_word_2_vec(docList, fileName, data_path):
    word_dict,participle_arr = participle_to_label(docList)
    f = open("work\\datasets\\dict1_txt.txt","w")
    f.write(str(word_dict))
    tf_method(word_dict,participle_arr,fileName,data_path)
        

def tf_method(word_dict, participle_arr,fileName,data_path):
    participle_arr = tf(word_dict,participle_arr)
    # 计算词向量
    files = open(data_path+fileName, "w",encoding="utf-8")
    for participle_word in participle_arr:
        str1 = ""
        for i in participle_word:
            str1 += ","+str(i)
        str1 = str1.strip(",")
        files.write(str1+ "\n")
    files.flush()

def create_dict(fileName,data_path,filePath):
    docList = []
    for doc in open(filePath):
        docList.append(doc)
    read_file_word_2_vec(docList=docList, fileName=fileName, data_path=data_path)

def write_classifiy(strs, label, data_path, files):
    strClass = ",".join(strs.strip("\n").split())
    str2 = strClass + "\t" + str(label)
    
    files.write(str2)  


# 获取字典的长度
def get_dict_len(dict_path):
    with open(dict_path, 'r', encoding='utf-8') as f:
        line = eval(f.readlines()[0])

    return len(line.keys())