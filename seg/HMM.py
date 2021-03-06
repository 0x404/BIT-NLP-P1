'''
author: 0x404
Date: 2021-10-15 19:57:42
LastEditTime: 2021-10-19 12:33:07
Description: 
'''

import os
import time
import pickle
import numpy as np
import seg.algorithm as algorithm

def loadHMMSegData(path, n = 100000):
    """
    加载使用HMM进行分词所需的训练集
    :param path: 源文件地址
    :return [sentence1, sentence2, ... ]    sentence = [{"text" : word1, "tag", tag1}, {"text" : word2, "tag", tag2}]
    """
    file = open(path, mode="r", encoding="utf-8")
    segData = []
    for id, line in enumerate(file):
        if id >= n:
            break
        line = line.strip()
        line = line.split(" ")
        if (len(line) == 1):
            print (id)
            print (line)
        text, tag = line[0], line[1]
        data = []
        for i in range(len(text)):
            data.append({"text" : text[i], "tag" : tag[i]})
        segData.append(data)
    return segData

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
    tagId = {"B" : 0, "M" : 1, "E" : 2, "S" : 3}
    idTag = {0 : "B", 1 : "M", 2 : "E", 3 : "S"}
    return tagId, idTag

def decoder(input):
    """
    解码器，将HMM带标签的结果解码为分词形式
    :param input: HMM结果，形如['沉/B', '重/E', '的/S', '双/B', '重/E', '使/B', '命/E']
    :return: 分词结果，形容["沉重", "的", "双重", "使命]
    """
    result = []
    now = ""
    for i in range(len(input)):
        word = input[i]
        text = word[0 : len(word) - 2]
        tag = word[-1]
        now += text
        if tag in ("S", "E") or i == len(input) - 1:
            result.append(now)
            now = ""
    return result

def cut(sentences, saveModel = False, useModel = False, progressBar = False):
    """
    使用HMM对输入进行分词（默认进行训练后分词）
    :param sentences: 待分词向量或矩阵[[sentence1], [sentence2], ... ]
    :param saveModel: 将训练的模型保存到本地
    :param useModel:  不进行训练，使用本地保存的模型进行分词
    :return: 分词后的结果矩阵[[sentence1], [sentence2], ... ]   sentence = [[word1], [word2], ... ]
    """
    if isinstance(sentences, str):  # 如果输入为一个一维向量，转成矩阵形式
        sentences = [sentences]
    model = {}
    if useModel:
        if os.path.exists("seg\\wordSegmentMoelHMM.pkl") == False:
            raise Exception("cut: 模型不存在，无法加载！")
        file = open("seg\\wordSegmentMoelHMM.pkl", mode="rb")
        model = pickle.load(file)
        file.close()
    else:
        samples = loadHMMSegData("data\\seg-processed\\msr_train.txt")
        tagId, idTag = generateTagMap()

        begin = generateBegin(samples, tagId)
        trans = generateTrans(samples, tagId)
        emit = generateEmit(samples, tagId)

        model = {"begin" : begin, "trans" : trans, "emit" : emit, "tagId" : tagId, "idTag" : idTag}
    
    cutResult = []
    if progressBar:     # 显示进度条以及计算时间
        print ("开始分词".center(58, "-"))
        caseSum = len(sentences)
        counter = 0
        Len = 50
        startTime = time.perf_counter()
        for sentence in sentences:
            counter += 1
            viterbiResult = algorithm.viterbi(sentence, model["begin"], model["trans"], model["emit"], model["tagId"], model["idTag"])
            cutResult.append(decoder(viterbiResult))
            finished = int(counter * Len / caseSum)
            a = "*" * finished
            b = "." * (Len - finished)
            c = (finished / Len) * 100
            curTime = time.perf_counter() - startTime
            if counter == caseSum:
                print ("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, curTime))
            else:
                print ("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, curTime), end="")
        print ("分词完成".center(58, "-"))
    else:
        for sentence in sentences:
            viterbiResult = algorithm.viterbi(sentence, model["begin"], model["trans"], model["emit"], model["tagId"], model["idTag"])
            cutResult.append(decoder(viterbiResult))
    
    if saveModel:
        file = open("seg\\wordSegmentMoelHMM.pkl", mode="wb")
        pickle.dump(model, file)
        file.close()
    return cutResult


def main():
    res = cut("思考一下这篇文章的大意", useModel=False)
    print (res)
if __name__ == "__main__":
    main()