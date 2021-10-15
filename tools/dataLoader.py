'''
author: 0x404
Date: 2021-10-13 20:12:16
LastEditTime: 2021-10-15 14:40:29
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

def loadSegData(n, path):
    """
    加载分词测试集
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

def loadPosData(n, path):
    """
    加载词性标注数据集
    :param n: 加载的句子数
    :param path: 数据集路径
    :return: [[sentence1], [sentence2], ... ]   sentence = [{"text":word1, "tag":tag1}, {"text":word2, "tag":tag2}, ...]
    """
    file = open(path, mode="r", encoding="utf-8")
    posData = []
    for id, line in enumerate(file):
        if id >= n:
            break
        line = line.strip()
        line = line.split("	")
        data = []
        for word in line:
            pos = word.rfind("/", 0, len(word))
            data.append({"text" : word[0 : pos], "tag" : word[pos + 1 : ]})
        posData.append(data)
    return posData

