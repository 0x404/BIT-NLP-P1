'''
author: 0x404
Date: 2021-10-15 20:11:44
LastEditTime: 2021-10-15 22:54:41
Description: 
'''
def generateTrainData(sourcePath, savePath):
    """
    生成HMM分词任务的训练数据
    :param sourcePath: 源文件路径
    :param savaPath: 生成数据保存文件
    :return: 
    """
    
    file = open(sourcePath, mode="r", encoding="utf-8")

    textData, tagData = [], []

    for line in file:
        line = line.strip()
        line = line.split(" ")
        text, tag = "", ""
        for word in line:
            if word == " " or len(word) == 0:
                continue
            word = word.strip()
            # print (word, len(word))
            if len(word) == 1:
                tag += "S"
            else:
                tag += "B"
                tag += "M" * (len(word) - 2)
                tag += "E"
            text += word
        if (len(text) > 0):
            textData.append(text)
            tagData.append(tag)
    file.close()
    file = open(savePath, mode="w", encoding="utf-8")
    for i in range(len(textData)):
        file.writelines(textData[i] + " " + tagData[i] + "\n")
    file.close()

def processRawData(sourcePath, savePath):
    file = open(sourcePath, mode="r", encoding="utf-8")
    save = open(savePath, mode="w", encoding="utf-8")
    for line in file:
        line = line.strip()
        line = line.split("  ")

        output = ""
        for word in line:
            word = word.strip()
            if len(word) >= 1 and word != " ":
                # print (word, len(word))
                output += word + " "
        output = output.strip()
        save.writelines(output + "\n")
    file.close()
    save.close()

def main():
    processRawData("..\\data\\msr_train.txt", "..\\data\\seg-processed\\a.txt")
    generateTrainData("..\\data\\seg-processed\\a.txt", "..\\data\\seg-processed\\msr_train.txt")


if __name__ == "__main__":
    main()