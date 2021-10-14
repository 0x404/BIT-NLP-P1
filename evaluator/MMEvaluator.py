'''
author: 0x404
Date: 2021-10-14 13:48:35
LastEditTime: 2021-10-14 16:02:39
Description: 
'''

import time
import tools.dataLoader as dataLoader
import seg.MM as MM
import util.helper as helper

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
    
    testData, ansData = dataLoader.loadTestData(n, path)
    
    resMM = []
    if mode == "FMM":
        resMM = MM.FMM(testData, dic)
    elif mode == "RMM":
        resMM = MM.RMM(testData, dic)
    else:
        resMM = MM.BMM(testData, dic)
    
    predData = []
    for item in resMM:
        predData.append(helper.getIntervals(item))
    
    sizeA, sizeB, sizeIntersect = 0, 0, 0

    for i in range(len(ansData)):
        sizeA += len(ansData[i])
        sizeB += len(predData[i])
        sizeIntersect += helper.getIntersectCount(ansData[i], predData[i])
    
    p = sizeIntersect / sizeB
    r = sizeIntersect / sizeA
    f = 2 * p * r / (p + r)

    print ("使用{}算法进行测试，测试集规模为{}, 测试共进行{:.2f}s".format(mode, n, time.time() - startTime))
    return p, r, f


