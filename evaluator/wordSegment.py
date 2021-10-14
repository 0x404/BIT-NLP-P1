'''
author: 0x404
Date: 2021-10-14 13:48:35
LastEditTime: 2021-10-14 14:54:28
Description: 
'''

import seg.MM as MM

def getIntervals(text):
    """
    返回分词结果的区间表示
    :param text: 分词后的列表
    :return: 区间表示的列表
    """
    ans = []
    sumL = 0
    for w in text:
        ans.append((sumL, sumL + len(w) - 1))
        sumL = sumL + len(w)
    return ans

def getIntersectCount(x, y):
    counterX, counterY = {}, {}
    for interval in x:
        if interval not in counterX.keys():
            counterX[interval] = 0
        else:
            counterX[interval] += 1
    for interval in y:
        if interval not in counterY.keys():
            counterY[interval] = 0
        else:
            counterY[interval] += 1
    ans = 0
    for key in counterX.keys():
        if key in counterY.keys():
            ans += 1
    return ans

def dataLoader(n):
    """
    加载测试集
    :param n: 测试集中的句子数
    :return: (testData, ansData)
    """
    file = open("data\\msr_train.txt", mode="r", encoding="utf-8")
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
        ansData.append(getIntervals(ansItem))
        
    file.close()
    return testData, ansData

def evaluateFMM(n, dic):
    testData, ansData = dataLoader(n)
    resFMM = MM.FMM(testData, dic)
    predData = []
    for item in resFMM:
        predData.append(getIntervals(item))
    
    sizeA, sizeB, sizeIntersect = 0, 0, 0

    for i in range(len(ansData)):
        sizeA += len(ansData[i])
        sizeB += len(predData[i])
        sizeIntersect += getIntersectCount(ansData[i], predData[i])
    
    p = sizeIntersect / sizeB
    r = sizeIntersect / sizeA
    f = 2 * p * r / (p + r)

    return p, r, f


