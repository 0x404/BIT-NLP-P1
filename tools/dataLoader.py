'''
author: 0x404
Date: 2021-10-13 20:12:16
LastEditTime: 2021-10-14 13:32:33
Description: 
'''


def loadDictionary(path):
    '''读取字典文件，返回单词列表'''
    file = open(path, mode="r", encoding="utf-8")
    wordList = []
    for line in file:
        line = line.split('	')
        wordList.append(line[0])
    return wordList

def loadTestSet(path):
    """
    读取测试集
    :return: [[sentenc1], [sentence2], ... ]
    """
    file = open(path, mode="r", encoding="utf-8")
    result = []
    for line in file:
        result.append(line)
    return result

