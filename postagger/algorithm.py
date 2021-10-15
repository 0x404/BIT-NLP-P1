'''
author: 0x404
Date: 2021-10-15 15:14:01
LastEditTime: 2021-10-15 16:50:00
Description: 
'''

def viterbi(observation, begin, trans, emit, tagId, idTag):
    """
    利用维特比算法，计算词性标注
    :param observation: 待标注的句子，如["寂静", "如", "雾", "缓缓", "漫", "开"]
    :param begin: HMM初始概率向量
    :param trans: HMM转移矩阵
    :param emit:  HMM发射矩阵
    :param tagId: tag到正数下标的map
    :param idTag: 正数下标到tag的map
    :return: 标注结果，如["寂静/a", "如/v", "雾/n", "缓缓/d", "漫/v", "开/v"]
    """
    t = len(observation)

    dp = [[float('-INF') for i in range(len(tagId))] for _ in range(2)]     # dp[i][j]表示到第i层当前状态为j时的最大概率，考虑dp[i][j]仅与dp[i-1][k]有关，故使用滚动数组
    ls = [[-1 for i in range(len(tagId))] for _ in range(t)]                # ls[i][j]为当前再第i层，状态为j，上一步由i - 1的哪个状态转移而来
    
    for i in range(len(tagId)):
        if observation[0] in emit[i].keys():
            dp[0][i] = begin[i] + emit[i][observation[0]]
        else:
            dp[0][i] = begin[i] + float('-INF')     # 如果状态i到第一个词的发射概率为0，则记为负无穷
    
    for i in range(t - 1):
        pre, now = i, i + 1

        for j in range(len(tagId)): 
            dp[now & 1][j] = float('-INF')  # 清空当前dp数组

        for preS in range(len(tagId)):  # 枚举前一个状态
            for nowS in range(len(tagId)):  # 枚举当前状态

                prob = 0    # 计算转移概率
                if observation[now] not in emit[nowS].keys():
                    prob = dp[pre & 1][preS] + trans[preS][nowS] + float('-INF')
                else:
                    prob = dp[pre & 1][preS] + trans[preS][nowS] + emit[nowS][observation[now]]

                if prob > dp[now & 1][nowS]:
                    dp[now & 1][nowS] = prob    #更新dp的最大值
                    ls[now][nowS] = preS        #维护ls数组
    
    ans = ["" for i in range(t)]    # 答案标签

    maxProb = float('-INF')
    state = -1
    for i in range(len(tagId)):     
        if dp[(t - 1) & 1][i] >= maxProb:   # 找到最后一个位置概率最大的状态
            maxProb = dp[(t - 1) & 1][i]
            state = i
    
    i = t - 1
    while i >= 0 and state != -1:   # 从后往前，通过ls数组逆推，得到答案标签数组
        ans[i] = idTag[state]
        state = ls[i][state]
        i -= 1

    res = observation[ : ]
    for i in range(len(res)):
        res[i] += "/" + ans[i]      # 组和成["寂静/a", "如/v", "雾/n", "缓缓/d", "漫/v", "开/v"]格式
    return res





                
