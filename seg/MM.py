'''
author: 0x404
Date: 2021-10-13 21:12:59
LastEditTime: 2021-10-15 13:09:34
Description: 最长匹配算法，分别实现正向最长匹配、逆向最长匹配、双向最长匹配
'''
import tools.trieTree as trieTree

def FMM(sentences, dic):
    """
    使用正向最长匹配进行分词
    :param sentence: 待分词的句子列表
    :param dic: 参考的词典列表
    :return: 返回分词结果的矩阵形式
    """
    maxLen = 0
    for word in dic:
        maxLen = max(maxLen, len(word)) # 出于效率考虑，窗口的最大长度为词典中词的最长长度

    result = []
    trie = trieTree.Trie(dic)   # 使用trie树优化算法时间复杂度

    for sentence in sentences:
        i = 0
        ans = []
        while i < len(sentence):
            pos = min(i + maxLen - 1, len(sentence) - 1)
            while trie.isExist(sentence[i : pos + 1]) == False and pos > i:
                pos = pos - 1
                if pos == i:
                    break
            ans.append(sentence[i : pos + 1])
            i = pos + 1
        result.append(ans)
    return result

def RMM(sentences, dic):
    """
    使用逆向最长匹配进行分词
    :param sentence: 待分词的句子列表
    :param dic: 参考的词典列表
    :return: 返回分词结果的矩阵形式
    """
    maxLen = 0
    for word in dic:
        maxLen = max(maxLen, len(word)) # 出于效率考虑，窗口的最大长度为词典中词的最长长度
    
    result = []
    trie = trieTree.Trie(dic)    # 使用trie树优化算法时间复杂度

    for sentence in sentences:
        i = len(sentence) - 1
        ans = []
        while i >= 0:
            pos = max(i - maxLen + 1, 0)
            while trie.isExist(sentence[pos : i + 1]) == False and pos < i:
                pos = pos + 1
                if pos == i:
                    break
            ans.append(sentence[pos : i + 1])
            i = pos - 1
        ans.reverse()
        result.append(ans)
    return result

def BMM(sentences, dic):
    """
    使用双向最长匹配进行分词
    :param sentence: 待分词的句子列表
    :param dic: 参考的词典列表
    :return: 返回分词结果的矩阵形式
    """
    result = []
    resFMMSet = FMM(sentences, dic)
    resRMMSet = RMM(sentences, dic)
    for i in range(len(sentences)):
        resFMM = resFMMSet[i]
        resRMM = resRMMSet[i]
        if len(resFMM) < len(resRMM):
            result.append(resFMM)
        elif len(resRMM) < len(resFMM):
            result.append(resRMM)
        else:
            counterFMM = sum(1 for w in resFMM if len(w) == 1)
            counterRMM = sum(1 for w in resRMM if len(w) == 1)
            if counterFMM < counterRMM:
                result.append(resFMM)
            else:
                result.append(resRMM)
    return result
    
