'''
author: 0x404
Date: 2021-10-14 20:49:58
LastEditTime: 2021-10-15 13:36:22
Description: 
'''



from os import popen


def processData(sourcePath, savePath):
    """
    预处理数据，把形如[贵州/ns	省委/n]/nt 转换成 贵州/ns	省委/n
    :param sourcePath: 源文件地址
    :param savePath: 转换后文件保存地址
    :return: 
    """
    file = open(sourcePath, mode="r", encoding="utf-8")
    save = open(savePath, mode="w", encoding="utf-8")
    for line in file:
        line = line.strip()
        line = line.split("	")
        
        for i in range(len(line)):
            pos = line[i].rfind("]/", 0, len(line[i]))
            if pos != -1 and pos != 0:
                flag = True
                j = i - 1
                while flag:
                    if line[j][0] == "[":
                        line[j] = line[j][1:]
                        flag = False
                    j -= 1
                line[i] = line[i][0 : pos]
        
        lineProcessed = ""
        for w in line:
            lineProcessed += w + "	"
        lineProcessed = lineProcessed[0 : len(lineProcessed) - 1] + '\n'
        save.writelines(lineProcessed)
    file.close()


def processTag(sourcePath, savePath):
    """
    加载tag集合
    :param sourcePath: 文本文件路径
    :param savePath: tag集合存储路径
    :return: 
    """
    tagSet = []
    file = open(savePath, mode="r", encoding="utf-8")
    for line in file:
        line = line.strip()
        tagSet = line.split("	")
    file.close()

    file = open(sourcePath, mode="r", encoding="utf-8")
    for line in file:
        line = line.strip()
        line = line.split("	")
        for word in line:
            pos = word.rfind("/", 0, len(word))
            tag = word[pos + 1 : ]
            if tag not in tagSet:
                tagSet.append(tag)
    file.close()

    output = ""
    for tag in tagSet:
        output += tag + "	"
    output = output[0 : len(output) - 1] + '\n'

    file = open(savePath, mode="w", encoding="utf-8")
    file.writelines(output)
    file.close()




def main():
    processData("..\\data\\199801-test.txt", "..\\data\\pos-processed\\199801-test.txt")
    processData("..\\data\\199801-train.txt", "..\\data\\pos-processed\\199801-train.txt")
    processTag("..\\data\\199801-test.txt", "..\\data\\pos-processed\\tagSet.txt")
    processTag("..\\data\\199801-train.txt", "..\\data\\pos-processed\\tagSet.txt")

if __name__ == "__main__":
    main()
                

