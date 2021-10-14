'''
author: 0x404
Date: 2021-10-14 20:49:58
LastEditTime: 2021-10-14 21:23:57
Description: 
'''



def processData(sourcePath, savePath):
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


def main():
    processData("..\\data\\199801-test.txt", "..\\data\\pos-processed\\199801-test.txt")
    processData("..\\data\\199801-train.txt", "..\\data\\pos-processed\\199801-train.txt")

if __name__ == "__main__":
    main()
                

