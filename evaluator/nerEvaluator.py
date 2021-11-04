'''
author: 0x404
Date: 2021-11-04 19:22:50
LastEditTime: 2021-11-04 20:41:13
Description: 
'''

import ner.HMM as HMM

def evaluate(n = 10000):
    """
    命名实体识别评测
    :param n: 评测前n个句子, 默认全部评测
    :return: precision, recall, f1-socre
    """
    nerData = HMM.loadHMMNERData("data\\ner-processed\\199801-test.txt")
    
    testData = []
    ansData = []
    for line in nerData:
        testItem = []
        ansItem = {"people" : [], "location" : [], "organization" : []}
        for w in line:
            testItem.append(w["text"])
        i = 0
        while i < len(line):        # 统计每个句子中的实体
            if line[i]["tag"] == 'O':
                i += 1
                continue
            elif line[i]["tag"] == "S_nr":
                ansItem["people"].append(line[i]["text"])
            elif line[i]["tag"] == "S_ns":
                ansItem["location"].append(line[i]["text"])
            elif line[i]["tag"] == "S_nt":
                ansItem["organization"].append(line[i]["text"])
            elif line[i]["tag"] == "B_ns":
                text = ""
                while line[i]["tag"] != "E_ns":
                    text += line[i]["text"]
                    i += 1
                text += line[i]["text"]
                ansItem["location"].append(text)
            elif line[i]["tag"] == "B_nt":
                text = ""
                while line[i]["tag"] != "E_nt":
                    text += line[i]["text"]
                    i += 1
                text += line[i]["text"]
                ansItem["organization"].append(text)
            elif line[i]["tag"] == "B_nr":
                text = ""
                while line[i]["tag"] != "E_nr":
                    text += line[i]["text"]
                text += line[i]["text"]
                ansItem["people"].append(text)
            i += 1
        testData.append(testItem)
        ansData.append(ansItem)
    
    if n < len(testData):
        testData = testData[0 : n]
        ansData = ansData[0 : n]

    predData = HMM.ner(testData, progressBar=True)  # 将测试数据丢到模型中预测

    corectNum = 0   # 预测成功的实体个数
    predNum = 0     # 预测的实体个数
    ansNum = 0      # 答案中的实体个数
    for i in range(len(predData)):

        predNum += len(ansData[i]["people"]) + len(ansData[i]["location"]) + len(ansData[i]["organization"])
        ansNum += len(predData[i]["people"]) + len(predData[i]["location"]) + len(predData[i]["organization"])
        
        for w in predData[i]["people"]:
            if w in ansData[i]["people"]:
                corectNum += 1

        for w in predData[i]["location"]:
            if w in ansData[i]["location"]:
                corectNum += 1

        for w in predData[i]["organization"]:
            if w in ansData[i]["organization"]:
                corectNum += 1
    
    p = corectNum / ansNum
    r = corectNum / predNum
    f = 2 * p * r / (p + r)
    return p, r, f

