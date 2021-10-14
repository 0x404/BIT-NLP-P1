'''
author: 0x404
Date: 2021-10-14 09:44:58
LastEditTime: 2021-10-14 11:00:09
Description: 
'''

import tools.trieTree as trieTree

INF = 1000000000

class Node():
    """网络节点类"""
    def __init__(self, val) -> None:
        """
        初始化节点
        :param val: 该节点的值
        :return: void
        """
        self.val = val      # 节点的值
        self.ind = 0        # 节点的入度
        self.prev = -1      # 节点的前驱
        self.to = []        # 节点的邻接点
        self.minDis = INF   # 从起点到当前节点的最短距离

    def add(self, next):
        """
        向当前节点添加一个节点
        :param: 添加的节点
        :return: void
        """
        self.to.append(next)
        next.ind = next.ind + 1

class Net():
    """网络类"""
    def __init__(self, text, dic) -> None:
        """
        初始化网络类
        :param text: 待分词的句子
        :param dic: 参考的词典
        :return: void
        """
        self.text = text    # 待分词的句子
        self.trie = trieTree.Trie(dic)          # 根据词典建立的trie树
        self.maxLen = max(len(w) for w in dic)  # 词典中单词的最长长度

        self.v = [Node(i) for i in range(len(text) + 1)]    # 网络中节点集合
        self.v[0].minDis = 0    # 初始化第一个点的距离

        self.__build()  # 构建网络

    def __build(self):
        """构建网络"""
        i = 0
        while i < len(self.text):
            for length in range(self.maxLen):
                if i + length >= len(self.text):
                    break
                if self.trie.isExist(self.text[i : i + length + 1]):
                    self.v[i].add(self.v[i + length + 1])
            i = i + 1

        for i in range(len(self.v) - 1):
            self.v[i].add(self.v[i + 1])

        self.__topsort() # 构建完成后通过按照拓扑序计算最短路径

    def __topsort(self):
        """拓扑排序"""
        for i in range(len(self.v) - 1):
            for adj in self.v[i].to:
                if self.v[i].minDis + 1 < adj.minDis:
                    adj.minDis = self.v[i].minDis + 1
                    adj.prev = i
        
        
    def getResult(self):
        """返回分词结果"""
        result = []
        now = len(self.text) # 从后往前，根据节点的前驱节点遍历
        
        while now > 0:
            prev = self.v[now].prev
            result.append(self.text[prev : now])
            now = prev
        
        result.reverse()    # 由于逆向遍历，需要对结果逆序处理
        return result

def splitByShortPath(text, dic):
    """
    使用最短路径法进行分词
    :param text: 待分词的句子
    :param dic: 参考的词典
    :return: 返回分词结果的列表形式
    """
    net = Net(text, dic)
    return net.getResult()
        

