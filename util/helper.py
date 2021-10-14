'''
author: 0x404
Date: 2021-10-14 15:54:13
LastEditTime: 2021-10-14 16:01:37
Description: 集合操作
'''

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
    """
    返回两个集合的交集的数量
    :param x: 集合x（列表形式）
    :param y: 集合y (列表形式)
    :return: 交集的数量
    """
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