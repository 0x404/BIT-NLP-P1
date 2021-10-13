'''
author: 0x404
Date: 2021-10-13 21:12:59
LastEditTime: 2021-10-13 21:45:50
Description: 最长匹配算法
'''
import tools.trieTree as trieTree

def FMM(sentence, dic):
    """
    使用正向最长匹配进行分词
    :param sentence: 待分词的句子
    :param dic: 参考的词典列表
    :return: 返回分词结果的列表形式
    """
    maxLen = 0
    for word in dic:
        maxLen = max(maxLen, len(word)) # 出于效率考虑，窗口的最大长度为词典中词的最长长度

    result = []
    trie = trieTree.Trie(dic)   # 使用trie树优化算法时间复杂度

    i = 0
    while i < len(sentence):
        pos = min(i + maxLen - 1, len(sentence) - 1)
        while trie.isExist(sentence[i : pos + 1]) == False:
            pos = pos - 1
            if pos == i:
                break
        result.append(sentence[i : pos + 1])
        i = pos + 1
    return result

def RMM(sentence, dic):
    """
    使用逆向最长匹配进行分词
    :param sentence: 待分词的句子
    :param dic: 参考的词典列表
    :return: 返回分词结果的列表形式
    """
    
    maxLen = 0
    for word in dic:
        maxLen = max(maxLen, len(word)) # 出于效率考虑，窗口的最大长度为词典中词的最长长度
    
    result = []
    trie = trieTree.Trie(dic)    # 使用trie树优化算法时间复杂度

    i = len(sentence) - 1
    while i >= 0:
        pos = max(i - maxLen + 1, 0)
        while trie.isExist(sentence[pos : i + 1]) == False:
            pos = pos + 1
            if pos == i:
                break
        result.append(sentence[pos : i + 1])
        i = pos - 1
    result.reverse()    # 逆向最长匹配的分词结果需要逆序
    return result


