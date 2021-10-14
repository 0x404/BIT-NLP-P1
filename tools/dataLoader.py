'''
author: 0x404
Date: 2021-10-13 20:12:16
LastEditTime: 2021-10-14 16:01:23
Description: 
'''
import util.helper as helper

def loadDictionary(path):
    '''读取字典文件，返回单词列表'''
    file = open(path, mode="r", encoding="utf-8")
    wordList = []
    for line in file:
        line = line.split('	')
        wordList.append(line[0])
    file.close()
    return wordList

def loadTestData(n, path):
    """
    加载测试集
    :param n: 测试集中的句子数
    :param path: 测试集路径
    :return: (testData, ansData)
    """
    file = open(path, mode="r", encoding="utf-8")
    testData, ansData = [], []
    for id, line in enumerate(file):
        if id >= n:
            break
        line = line.strip()
        ansItem = line.split("  ")
        testItem = ""
        for c in line:
            if c != " ":
                testItem = testItem + c
        testData.append(testItem)
        ansData.append(helper.getIntervals(ansItem))
        
    file.close()
    return testData, ansData

