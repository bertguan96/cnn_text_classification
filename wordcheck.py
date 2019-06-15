import re, collections
import time


# 读取big.txt 内容，big.txt就是原理中提到的语料库，这个不是死的
open_r = open("wordcheck.txt", 'r')
big_info = open_r.read()
open_r.close()

alphabet = 'abcdefghijklmnopqrstuvwxyz'


# 提炼出单词
def words(info):
    return re.findall("[a-z]+", info.lower())


# 计算词出现的次数
def wordIndex(wordtext):
    words = {}
    for word in wordtext:
        if word in words:
            words[word] = words[word] + 1
        else:
            words[word] = 1
    return words


# 调用方法得到每个单词使用的次数
words_map = wordIndex(words(big_info))


# 如果存在该单词则返回该单词
def known(word):
    word1 = []
    for word_one in word:
        if word_one in words_map:
            word1.append(word_one)
    return word1


# 一次纠正得到一个集合
def knomn_edit1(words):
    edit1_word = []
    n = len(words)
    for j in range(n):
        # print(i)
        word = words[j]
        m = len(word)
        for i in range(m):
            if i != m - 1:
                edit1_word.append(word[0:i] + word[i + 1:])  # 删
                if i != m - 2:
                    edit1_word.append(word[0:i] + word[i + 1] + word[i] + word[i + 2:])  # 移动
                else:
                    edit1_word.append(word[0:i] + word[i + 1] + word[i])  # 移动
                for ch in alphabet:
                    edit1_word.append(word[0:i] + ch + word[i + 1:])  # 替换
                    edit1_word.append(word[0:i] + ch + word[i:])  # 插入
            else:
                edit1_word.append(word[0:(m - 1)])  # 删
                for ch in alphabet:
                    edit1_word.append(word[0:(m - 1)] + ch)  # 替换
                    edit1_word.append(word[0:m] + ch)  # 插入
    return edit1_word


# 二次纠正
def know_edit2(word):
    words1 = knomn_edit1(word)
    words2 = knomn_edit1(words1)
    edit2_word = []
    for word2 in words2:
        if word2 in words_map:
            edit2_word.append(word2)
    return edit2_word


#
def correct(word):
    canword = known([word]) or known(knomn_edit1([word])) or know_edit2([word])
    if len(canword) == 0:#如果两步纠正还是没得到正确单词，那么就默认返回输入的错误单词
        canword = [word]
        # print(canword)
        return canword[0]
    else:
        max_info = max(canword, key=lambda w: words_map[w])
        # print(str(max_info))
        return str(max_info)
    
