'''
author: 0x404
Date: 2021-10-14 13:48:35
LastEditTime: 2021-10-14 15:48:26
Description: 
'''
import time
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

def dataLoader(n, path):
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
        ansData.append(getIntervals(ansItem))
        
    file.close()
    return testData, ansData

def evaluate(mode, path, n, dic):
    """
    评测MM算法
    :param mode: 使用的算法(FMM, RMM, BMM)
    :param path: 测试集路径
    :param n: 选择测试集前n条进行测试
    :param dic: 参考的字典
    :return: precision, recall, f1-socre
    """
    startTime = time.time() # 计时器

    if mode not in ("FMM", "RMM", "BMM"):
        raise Exception("最长匹配算法：模式不存在")
    
    testData, ansData = dataLoader(n, path)
    
    resMM = []
    if mode == "FMM":
        resMM = MM.FMM(testData, dic)
    elif mode == "RMM":
        resMM = MM.RMM(testData, dic)
    else:
        resMM = MM.BMM(testData, dic)
    
    predData = []
    for item in resMM:
        predData.append(getIntervals(item))
    
    sizeA, sizeB, sizeIntersect = 0, 0, 0

    for i in range(len(ansData)):
        sizeA += len(ansData[i])
        sizeB += len(predData[i])
        sizeIntersect += getIntersectCount(ansData[i], predData[i])
    
    p = sizeIntersect / sizeB
    r = sizeIntersect / sizeA
    f = 2 * p * r / (p + r)

    print ("使用{}算法进行测试，测试集规模为{}, 测试共进行{:.2f}s".format(mode, n, time.time() - startTime))

    return p, r, f


