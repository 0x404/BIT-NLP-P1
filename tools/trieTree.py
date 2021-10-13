'''
author: 0x404
Date: 2021-10-13 20:29:22
LastEditTime: 2021-10-13 21:00:46
Description: 
'''


class Node():
    def __init__(self, val) -> None:
        """
        初始化trie树节点
        :param val: 当前节点的值
        :return: void
        """
        self.val = val
        self.son = {}
        self.isEnd = False

    def hasSon(self, val):
        """
        查询当前节点是否有一个子节点值为val
        :param val: 子节点的值
        :return: 如果存在，返回True；如果不存在，返回False
        """
        if val in self.son.keys():
            return True
        return False
    
    def getSon(self, val):
        """
        获得当前节点的值为val的子节点
        :param val: 子节点的值
        :return: 如果存在子节点，返回子节点；否则返回-1
        """
        if self.hasSon(val):
            return self.son[val]
        return -1

    def addSon(self, val):
        """
        向当前节点添加一个值为val的子节点
        :param val: 待添加的子节点的值
        :return: void
        """
        if self.hasSon(val):
            return
        self.son[val] = Node(val)

class Trie():
    def __init__(self, dic = []) -> None:
        """
        初始化trie树
        :param dic: 用于构造trie树的字典列表
        :return: void
        """
        self._topNode = Node(0)
        self.build(dic)
    
    def build(self, dic):
        """
        构建trie树
        :param dic: 用于构造trie树的字典列表
        :return: void
        """
        for word in dic:
            self.insert(word)

    def insert(self, word):
        """
        向trie树中插入词
        :param word: 插入的词
        :return: void
        """
        now = self._topNode
        for i in range(0, len(word)):
            if now.hasSon(word[i]) == False:
                now.addSon(word[i])
            now = now.getSon(word[i])
        now.isEnd = True
    
    def isExist(self, word):
        """
        查询单词是否存在
        :param word: 待查询的词
        :return: 存在返回True，不存在返回False
        """
        now = self._topNode
        for i in range(0, len(word)):
            if now.hasSon(word[i]) == False:
                return False
            now = now.getSon(word[i])
        return True