'''
author: 0x404
Date: 2021-10-15 15:14:01
LastEditTime: 2021-10-15 16:26:37
Description: 
'''

def viterbi(observation, begin, trans, emit, tagId, idTag):
    """
    利用维特比算法，计算词性标注
    :param observation: 待标注的句子，如[寂静, 如, 雾, 缓缓, 散, 开]
    :param begin: HMM初始概率向量
    :param trans: HMM转移矩阵
    :param emit:  HMM发射矩阵
    :param tagId: tag到正数下标的map
    :param idTag: 正数下标到tag的map
    :return: 标注结果，如[寂静/a, 如/v, 雾/n, 缓缓/d, 漫/v, 开/v]
    """
    t = len(observation)

    dp = [[float('-INF') for i in range(len(tagId))] for _ in range(2)]
    ls = [[-1 for i in range(len(tagId))] for _ in range(t)]
    
    for i in range(len(tagId)):
        if observation[0] in emit[i].keys():
            dp[0][i] = begin[i] + emit[i][observation[0]]
        else:
            dp[0][i] = begin[i] + float('-INF')
    
    for i in range(t - 1):
        pre, now = i, i + 1
        for j in range(len(tagId)):
            dp[now & 1][j] = float('-INF')

        for preS in range(len(tagId)):
            for nowS in range(len(tagId)):

                prob = 0
                if observation[now] not in emit[nowS].keys():
                    prob = dp[pre & 1][preS] + trans[preS][nowS] + float('-INF')
                else:
                    prob = dp[pre & 1][preS] + trans[preS][nowS] + emit[nowS][observation[now]]

                if prob > dp[now & 1][nowS]:
                    dp[now & 1][nowS] = prob
                    ls[now][nowS] = preS
    
    ans = ["" for i in range(t)]
    maxProb = float('-INF')
    state = -1

    for i in range(len(tagId)):
        if dp[(t - 1) & 1][i] >= maxProb:
            maxProb = dp[(t - 1) & 1][i]
            state = i
    
    i = t - 1
    while i >= 0 and state != -1:
        ans[i] = idTag[state]
        state = ls[i][state]
        i -= 1

    res = observation[ : ]
    for i in range(len(res)):
        res[i] += "/" + ans[i]
    return res





                
