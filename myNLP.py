'''
author: 0x404
Date: 2021-10-19 12:21:50
LastEditTime: 2021-10-19 13:52:28
Description: 
'''

import seg.HMM as segHMM
import seg.MM as segMM
import seg.shortPath as segShortPath
import postagger.HMM as posHMM
import ner.HMM as nerHMM
import evaluator.posEvaluator as posEvaluator
import evaluator.segEvaluator as segEvaluator
import tools.dataLoader as dataLoader

def cut(sentences, HMM = False, FMM = False, RMM = False, BMM = False, shortPath = False, progressBar = False, useModel = False):
    """
    分词
    :param sentences: 待分词字符串，一个字符串，或者一个字符串列表
    :param HMM: 使用HMM分词
    :param FMM: 使用FMM分词
    :param RMM: 使用RMM分词
    :param BMM: 使用BMM分词
    :param shortPath: 使用最短路径算法分词
    :param progressBar: 显示进度条
    :param useModel: 使用HMM时使用原有模型
    :return: 分词结果
    """
    if HMM + FMM + RMM + BMM + shortPath != 1:
        raise Exception("MyNLP-cut: 分词模式错误")
    
    if isinstance(sentences, str):  # 如果输入为一个字符串，转为一个字符串列表
        sentences = [sentences]

    if HMM:
        cutResult = segHMM.cut(sentences, saveModel=False, useModel=useModel, progressBar=progressBar)
        return cutResult
    
    dic = dataLoader.loadDictionary("data\\dictionary.txt")

    if FMM:
        cutResult = segMM.FMM(sentences, dic)
        return cutResult
    
    if RMM:
        cutResult = segMM.RMM(sentences, dic)
        return cutResult
    
    if BMM:
        cutResult = segMM.BMM(sentences, dic)
        return cutResult
    
    if shortPath:
        cutResult = segShortPath.splitByShortPath(sentences, dic)
        return cutResult

def tag(sentences, HMM = True, progressBar = False, useModel = False):
    """
    词性标注
    :param sentences: 待标注向量或矩阵
    :param HMM: 使用HMM进行标注（当前仅支持HMM）
    :param progressBar: 显示进度条
    :param useModel: 使用HMM时是否显示进度条
    :return: 标注结果
    """
    if isinstance(sentences[0], str): # 如果输入为一个向量 转为一个矩阵
        sentences = [sentences]
    tagResult = posHMM.tag(sentences, True, useModel=useModel, progressBar=progressBar)
    return tagResult

def ner(sentences, HMM = True, progressBar = False, useModel = False):
    """
    命名实体识别
    :param sentences: 待识别向量或矩阵
    :param HMM: 使用HMM进行命名实体识别（当前仅支持HMM）
    :param progressBar: 显示进度条
    :param useModel: 使用HMM时是否显示进度条
    :return: 标注结果
    """
    nerResult = nerHMM.ner(sentences, True, progressBar=progressBar, useModel=useModel)
    return nerResult

def evaluateTag(caseCount = 2000, HMM = True):
    """
    评测词性标注算法
    :param caseCount: 评测测试集中的前caseCount句，默认全部评测
    :HMM: 评测HMM算法表现（当前仅支持HMM）
    :return: precision, recall, f1-socre
    """
    precision, recall, f1 = posEvaluator.evaluate(caseCount)
    return precision, recall, f1

def evaluateCut(caseCount = 100000, HMM = False, BMM = False, RMM = False, FMM = False, shortPath = False):
    """
    评测分词算法
    :param caseCount: 评测测试中的前caseCount句，默认全部评测
    :HMM: 评测HMM算法的分词表现
    :BMM: 评测BMM算法的分词表现
    :RMM: 评测RMM算法的分词表现
    :FMM: 评测FMM算法的分词表现
    :shortPath: 评测最短路算法的分词表现
    :return: precision, recall, f1-score
    """
    if HMM + BMM + RMM + FMM + shortPath != 1:
        raise Exception("MyNLP-evaluateCut: 模式错误！")
    dic = dataLoader.loadDictionary("data\\dictionary.txt")
    testDataPath = "data\\msr_train.txt"
    if HMM:
        precision, recall, f1 = segEvaluator.evaluate("HMM", testDataPath, caseCount, dic)
    if BMM:
        precision, recall, f1 = segEvaluator.evaluate("BMM", testDataPath, caseCount, dic)
    if RMM:
        precision, recall, f1 = segEvaluator.evaluate("RMM", testDataPath, caseCount, dic)
    if FMM:
        precision, recall, f1 = segEvaluator.evaluate("FMM", testDataPath, caseCount, dic)
    if shortPath:
        precision, recall, f1 = segEvaluator.evaluate("shortPath", testDataPath, caseCount, dic)
    return precision, recall, f1
    