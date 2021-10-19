'''
author: 0x404
Date: 2021-10-16 18:41:14
LastEditTime: 2021-10-19 13:00:43
Description: 
'''
import os
import pickle
import time
import numpy as np
import ner.algorithm as algorithm

def loadHMMNERData(path, n = 100000):
    """
    加载使用HMM进行NER任务的数据
    :param path: BMEO标签数据路径
    :param n: 加载的句子数量
    :return: [sentence1, sentence2, ... ]    sentence = [{"text" : word1, "tag", tag1}, {"text" : word2, "tag", tag2}]
    """
    file = open(path, mode="r", encoding="utf-8")
    nerData = []
    for line in file:
        line = line.strip()
        line = line.split("	")
        sentence = []
        for w in line:
            w = w.split("/")
            sentence.append({"text" : w[0], "tag" : w[1]})
        nerData.append(sentence)
    return nerData[0 : n]

def normalize(matrix):
    """
    先对矩阵进行归一化，后对矩阵取对数
    :param matrix: 待归一化的矩阵
    :return: 处理后的矩阵
    """
    for i in range(len(matrix)):
        tot = sum(cnt for cnt in matrix[i])
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                matrix[i][j] = float('-INF')            # 如果概率为0，取对数后为负无穷
            else:
                matrix[i][j] = matrix[i][j] / tot
                matrix[i][j] = np.log(matrix[i][j])     # 否则归一化后取对数
    return matrix
    
def generateBegin(samples, tagID):
    """
    训练初始矩阵
    :param samples: 训练集[[sample1], [sample2], ... ]
    :param tagID: map[tag]->id
    :return: 训练完成的初始矩阵
    """
    begin = [0 for i in range(len(tagID))]
    for sample in samples:
        start = sample[0]
        begin[tagID[start["tag"]]] += 1
        
    begin = normalize([begin])[0]
    return begin

def generateTrans(samples, tagID):
    """
    训练转移矩阵
    :param samples: 训练集[[sample1], [sample2], ... ]
    :param tagID: map[tag]->id
    :return: 训练完成的转移矩阵
    """
    trans = [[0 for i in range(len(tagID))] for _ in range(len(tagID))]
    for sample in samples:
        if len(sample) < 2:
            continue
        prev = sample[0]
        for j in range(1, len(sample)):
            now = sample[j]
            trans[tagID[prev["tag"]]][tagID[now["tag"]]] += 1
            prev = now
    
    trans = normalize(trans)
    return trans

def generateEmit(samples, tagID):
    """
    训练发射矩阵
    :param samples: 训练集[[sample1], [sample2], ... ]
    :param tagID: map[tag]->id
    :return: 训练完成的转移矩阵
    """
    emit = [{} for i in range(len(tagID))] # 出于性能考虑，emit[i]是一个map而不是一个连续数组
    for sample in samples:
        for data in sample:
            text = data["text"]
            tag = data["tag"]
            if text not in emit[tagID[tag]].keys():
                emit[tagID[tag]][text] = 1
            else:
                emit[tagID[tag]][text] += 1
    
    # 由于使用map，无法直接调用normalize归一化
    for i in range(len(emit)):
        tot = 0
        for j in emit[i].keys():
            tot += emit[i][j]
        for j in emit[i].keys():
            if emit[i][j] == 0:
                emit[i][j] = float('-INF')
            else:
                emit[i][j] = emit[i][j] / tot
                emit[i][j] = np.log(emit[i][j])
    
    return emit

def generateTagMap():
    tagId = {"B_nr" : 0, "B_ns" : 1, "B_nt" : 2,
             "M_nr" : 3, "M_ns" : 4, "M_nt" : 5,
             "E_nr" : 6, "E_ns" : 7, "E_nt" : 8,
             "S_nr" : 9, "S_ns" : 10, "S_nt" : 11,
             "O": 12}
    idTag = {}
    for key in tagId.keys():
        idTag[tagId[key]] = key
    return tagId, idTag

def decoder(input):
    """
    对viterbi算法的结果进行解码
    :param input: viterbi算法的结果, 形如['中共中央/B_nt', '政治局/E_nt', '常委/O', '李岚清/S_nr']
    :return: 人名集合nrSet, 地名nsSet, 机构名ntSet
    """
    f = {"nr" : 0, "ns" : 1, "nt" : 2}
    result = [[], [], []]
    

    for i in range(len(input)):
        input[i] = input[i].split("/")

    i = 0
    while i < len(input):
        text = input[i][0]
        tag = input[i][1]
        if tag in ("S_nr", "S_nt", "S_ns"):
            result[f[tag[2:]]].append(text)
            i += 1
            continue
        elif tag in ("B_nr", "B_nt", "B_ns"):
            now = ""
            while i < len(input) and input[i][1][0] != "E":
                now += input[i][0]
                i += 1
            if i < len(input):
                now += input[i][0]
            if i == len(input):
                i -= 1
            result[f[input[i][1][2:]]].append(now)
        i += 1
    return result[0], result[1], result[2]

def ner(sentences, saveModel = False, useModel = False, progressBar = False):
    """
    使用HMM对输入进行命名实体识别（默认训练后进行实体识别）
    :param sentences: 待识别向量或矩阵[[sentence1], [sentence2], ... ]   sentence = [[word1], [word2], ... ]
    :param saveModel: 将训练的模型保存到本地
    :param useModel:  不进行训练，使用本地保存的模型进行词性命名实体识别
    :param progressBar: 显示当前标注进度
    :return: 结果矩阵[[result1], [result2], ... ]   result = {"location" : [], "people" : [], "organization" : []}
    """

    if isinstance(sentences[0], str):   # 如果输入为一维向量，转成一个矩阵处理
        sentences = [sentences]
    model = {}
    if useModel:    
        if os.path.exists("D:\\School\\大三\\自然语言处理\\作业\\Project1\\ner\\nerModelHMM.pkl") == False:
            raise Exception("tag: 模型不存在，无法加载！")

        file = open("D:\\School\\大三\\自然语言处理\\作业\\Project1\\ner\\nerModelHMM.pkl", mode="rb")
        model = pickle.load(file)
        file.close()
    else:
        samples = loadHMMNERData("data\\ner-processed\\199801-train.txt")
        tagId, idTag = generateTagMap()

        begin = generateBegin(samples, tagId)
        trans = generateTrans(samples, tagId)
        emit = generateEmit(samples, tagId)

        model = {"begin" : begin, "trans" : trans, "emit" : emit, "tagId" : tagId, "idTag" : idTag}
    
    nerResult = []

    if progressBar:     # 显示进度条以及计算时间
        print ("开始识别".center(58, "-"))
        caseSum = len(sentences)
        counter = 0
        Len = 50
        startTime = time.perf_counter()
        for sentence in sentences:
            counter += 1
            viterbiResult = algorithm.viterbi(sentence, model["begin"], model["trans"], model["emit"], model["tagId"], model["idTag"])
            people, location, organization = decoder(viterbiResult)
            nerResult.append({"people" : people, "location" : location, "organization" : organization})
            finished = int(counter * Len / caseSum)
            a = "*" * finished
            b = "." * (Len - finished)
            c = (finished / Len) * 100
            curTime = time.perf_counter() - startTime
            if counter == caseSum:
                print ("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, curTime))
            else:
                print ("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, curTime), end="")

        print ("识别完成".center(58, "-"))
    else:
        for sentence in sentences:
            viterbiResult = algorithm.viterbi(sentence, model["begin"], model["trans"], model["emit"], model["tagId"], model["idTag"])
            people, location, organization = decoder(viterbiResult)
            nerResult.append({"people" : people, "location" : location, "organization" : organization})
    
    if saveModel:
        file = open("ner\\nerModelHMM.pkl", mode="wb")
        pickle.dump(model, file)
        file.close()

    return nerResult

if __name__ == "__main__":
    samples = loadHMMNERData("..\\data\\ner-processed\\199801-train.txt")
    tagId, idTag = generateTagMap()
    begin = generateBegin(samples, tagId)
    trans = generateTrans(samples, tagId)
    emit = generateEmit(samples, tagId)
    ans = algorithm.viterbi(["福建省"], begin, trans, emit, tagId, idTag)
    name, location, orgnization = decoder(ans)
    print (ans)
    print ("人名：", name)
    print ("地名：", location)
    print ("机构名：", orgnization)
    