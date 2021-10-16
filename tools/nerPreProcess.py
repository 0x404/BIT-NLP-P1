'''
author: 0x404
Date: 2021-10-16 18:28:48
LastEditTime: 2021-10-16 19:27:13
Description: 
'''


def generateBMEOData(sourcePath, savePath):
    """
    将199801文件转成BMEO标记
    :param sourcePath: 源文件地址 199801.txt
    :param savePath: 转换后保存的地址
    :return:
    """
    file = open(sourcePath, mode="r", encoding="utf-8")
    save = open(savePath, mode="w", encoding="utf-8")
    for line in file:
        line = line.strip()
        if len(line) <= 1:
            continue
        line = line.split("	")
        text = ["" for i in range(len(line))]
        tag = ["" for i in range(len(line))]
        for i in range(len(line)):
            pos = line[i].rfind("]/")

            if pos != -1:
                wTag = line[i][pos + 2 : ]
                if wTag in ("nr", "ns", "nt"):
                    text[i] = line[i][0 : pos]
                    text[i] = text[i][0 : text[i].rfind("/")]
                    tag[i] = "E_" + wTag

                    j = i - 1
                    while j >= 0:
                        if line[j][0] != '[':
                            pos = line[j].rfind("/")
                            tag[j] = "M_" + wTag
                            # text[j] = line[j][0 : pos]
                        elif line[j][0] == '[':
                            tag[j] = "B_" + wTag
                            # pos = line[j].rfind("/")
                            text[j] = text[j][1 : ]
                            break
                        j -= 1
                else:
                    text[i] = line[i][0 : pos]
                    wTag = text[i][text[i].rfind("/") + 1 : ]
                    text[i] = line[i][0 : text[i].rfind("/")]
                    if wTag in ("nr", "ns", "nt"):
                        tag[i] = "S_" + wTag
                    else:
                        tag[i] = "O"
                    j = i - 1
                    while j >= 0:
                        if line[j][0] == '[':
                            text[j] = text[j][1 : ]
                            break
                        j -= 1
            else:
                pos = line[i].rfind("/")
                wTag = line[i][pos + 1 : ]
                text[i] = line[i][0 : pos]
                if wTag in ("nr", "ns", "nt"):
                    tag[i] = "S_" + wTag
                else:
                    tag[i] = "O"
        # print (text, tag)
        output = ""
        for i in range(len(text)):
            output += text[i] + "/" + tag[i] + "	"
        output = output[0 : len(output) - 1] + "\n"
        save.writelines(output)
    file.close()
    save.close()

if __name__ == "__main__":
    generateBMEOData("..\\data\\199801-test.txt", "..\\data\\ner-processed\\199801-test.txt")
    generateBMEOData("..\\data\\199801-train.txt", "..\\data\\ner-processed\\199801-train.txt")
