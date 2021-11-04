'''
author: 0x404
Date: 2021-10-16 14:18:32
LastEditTime: 2021-11-04 20:41:28
Description: 
'''

import postagger.HMM as HMM


def evaluate(n = 5000):
    """
    词性标注评测
    :param n: 评测前n个句子, 默认全部评测
    :return: precision, recall, f1-socre
    """

    data = HMM.loadPosData("data\\pos-processed\\199801-test.txt")

    # 将加载的数据集分为待标注序列和标签答案序列
    testData, ansTag = [], []
    for line in data:
        tmpTest, tmpTag = [], []
        for w in line:
            tmpTest.append(w["text"])
            tmpTag.append(w["tag"])
        testData.append(tmpTest)
        ansTag.append(tmpTag)
    
    testData = testData[0 : n]  # 待标注序列，形式为[["铁路", "如何", "迎接"], ... ]
    ansTag = ansTag[0 : n]      # 标签答案序列，形式为[["n", "r", "v"], ... ]
    predData = HMM.tag(testData, useModel=True, progressBar=True) # HMM词性标注结果，形式为["铁路/n", "如何/r", "迎接/v"]
    predTag = []    # 将标注结果转成标签形式，形式为["n", "r", "v"]
    for line in predData:
        tmpTag = []
        for w in line:
            pos = w.rfind("/")
            tmpTag.append(w[pos + 1 : ])
        predTag.append(tmpTag)

    tagNum, predNum, correctNum = 0, 0, 0
    for i in range(len(ansTag)):
        tagNum += len(ansTag[i])
        predNum += len(predTag[i])
        for j in range(len(ansTag[i])):
            if ansTag[i][j] == predTag[i][j]:
                correctNum += 1

    p = correctNum / tagNum
    r = correctNum / predNum
    f = 2 * p * r / (p + r)

    return p, r, f