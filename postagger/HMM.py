'''
author: 0x404
Date: 2021-10-14 21:35:37
LastEditTime: 2021-10-16 16:05:10
Description: 
'''
# import tools.dataLoader as dataLoader
import numpy as np
import pickle
import os
import time
import algorithm as algorithm

def loadPosData(path, n = 1000000):
    """
    加载词性标注数据集
    :param n: 加载的句子数
    :param path: 数据集路径
    :return: [[sentence1], [sentence2], ... ]   sentence = [{"text":word1, "tag":tag1}, {"text":word2, "tag":tag2}, ...]
    """
    file = open(path, mode="r", encoding="utf-8")
    posData = []
    for id, line in enumerate(file):
        if id >= n:
            break
        line = line.strip()
        line = line.split("	")
        data = []
        for word in line:
            pos = word.rfind("/", 0, len(word))
            data.append({"text" : word[0 : pos], "tag" : word[pos + 1 : ]})
        posData.append(data)
    return posData

def generateTagMap(mode, para):
    """
    生成由tag到正数下标的map
    :param mode: 参数类型，file 或者 list
    :param para: 参数
    :return: map[tag] = id, map[id] = tag
    """

    tagID, idTag = {}, {}

    if mode not in ("file", "list"):
        raise Exception("生成tagMAP：模式错误")
    tagSet = para
    if mode == "file":
        file = open(para, mode="r", encoding="utf-8")
        for line in file:
            line = line.strip()
            tagSet = line.split("	")
        file.close()
    
    for i in range(len(tagSet)):
        tagID[tagSet[i]] = i
        idTag[i] = tagSet[i]

    return tagID, idTag

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


def tag(sentences, saveModel = False, useModel = False, progressBar = False):
    """
    使用HMM对输入进行词性标注（默认训练后进行词性标注）
    :param sentences: 待标注向量或矩阵[[sentence1], [sentence2], ... ]   sentence = [[word1], [word2], ... ]
    :param saveModel: 将训练的模型保存到本地
    :param useModel:  不进行训练，使用本地保存的模型进行词性标注
    :param progressBar: 显示当前标注进度
    :return: 词性标注后的结果矩阵[[sentence1], [sentence2], ... ]   sentence = [[word1/tag1], [word2/tag2], ... ]
    """

    if isinstance(sentences[0], str):   # 如果输入为一维向量，转成一个矩阵处理
        sentences = [sentences]
    model = {}
    if useModel:    
        if os.path.exists("D:\\School\\大三\\自然语言处理\\作业\\Project1\\postagger\\posTagerModelHMM.pkl") == False:
            raise Exception("tag: 模型不存在，无法加载！")

        file = open("D:\\School\\大三\\自然语言处理\\作业\\Project1\\postagger\\posTagerModelHMM.pkl", mode="rb")
        model = pickle.load(file)
        file.close()
    else:
        samples = loadPosData("..\\data\\pos-processed\\199801-train.txt")
        tagId, idTag = generateTagMap("file", "..\\data\\pos-processed\\tagSet.txt")

        begin = generateBegin(samples, tagId)
        trans = generateTrans(samples, tagId)
        emit = generateEmit(samples, tagId)

        model = {"begin" : begin, "trans" : trans, "emit" : emit, "tagId" : tagId, "idTag" : idTag}
    
    tagResult = []

    if progressBar:     # 显示进度条以及计算时间
        print ("开始标注".center(58, "-"))
        caseSum = len(sentences)
        counter = 0
        Len = 50
        startTime = time.perf_counter()
        for sentence in sentences:
            counter += 1
            tagResult.append(algorithm.viterbi(sentence, model["begin"], model["trans"], model["emit"], model["tagId"], model["idTag"]))
            finished = int(counter * Len / caseSum)
            a = "*" * finished
            b = "." * (Len - finished)
            c = (finished / Len) * 100
            curTime = time.perf_counter() - startTime
            if counter == caseSum:
                print ("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, curTime))
            else:
                print ("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, curTime), end="")

        print ("标注完成".center(58, "-"))
    else:
        for sentence in sentences:
            tagResult.append(algorithm.viterbi(sentence, model["begin"], model["trans"], model["emit"], model["tagId"], model["idTag"]))
    
    if saveModel:
        file = open("posTagerModelHMM.pkl", mode="wb")
        pickle.dump(model, file)
        file.close()

    return tagResult


def main():
    
    res = tag(["当前", "，", "康姝元元", "最最最最", "可爱"], useModel=True, progressBar=True)
    print (res)

if __name__ == "__main__":
    main()