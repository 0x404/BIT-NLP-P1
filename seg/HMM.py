'''
author: 0x404
Date: 2021-10-15 19:57:42
LastEditTime: 2021-10-15 23:12:44
Description: 
'''

from typing import Text
import numpy as np
import algorithm

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



def main():
    tagId, idTag = generateTagMap()
    samples = loadHMMSegData("..\\data\\seg-processed\\msr_train.txt")
    begin = generateBegin(samples, tagId)
    trans = generateTrans(samples, tagId)
    emit = generateEmit(samples, tagId)
    res = algorithm.viterbi("我喜欢你", begin, trans, emit, tagId, idTag)
    print (res)
    decode = decoder(res)
    print (decode)

if __name__ == "__main__":
    main()