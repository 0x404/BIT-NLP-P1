'''
author: 0x404
Date: 2021-10-14 13:48:35
LastEditTime: 2021-10-14 19:15:22
Description: 
'''

import time
import tools.dataLoader as dataLoader
import seg.MM as MM
import seg.shortPath as shortPath
import util.helper as helper

def evaluate(mode, path, n, dic):
    """
    评测MM算法
    :param mode: 使用的算法(FMM, RMM, BMM, shortPath)
    :param path: 测试集路径
    :param n: 选择测试集前n条进行测试
    :param dic: 参考的字典
    :return: precision, recall, f1-socre
    """
    startTime = time.time() # 计时器

    if mode not in ("FMM", "RMM", "BMM", "shortPath"):
        raise Exception("最长匹配算法：模式不存在")
    
    testData, ansData = dataLoader.loadTestData(n, path)
    
    res = []
    if mode == "FMM":
        res = MM.FMM(testData, dic)
    elif mode == "RMM":
        res = MM.RMM(testData, dic)
    elif mode == "BMM":
        res = MM.BMM(testData, dic)
    else:
        res = shortPath.splitByShortPath(testData, dic)

    print (res)

    predData = []
    for item in res:
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


