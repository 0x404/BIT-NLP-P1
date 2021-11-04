## BIT自然语言理解初步大作业一

## 当前已完成

* trie树
  * `tools/trieTree`
* 基于词典的分词算法：
  * `seg\MM`，包含FMM、BMM、RMM
  * `seg\shortPath`，基于最短路的词典分词算法
* 基于统计的分词算法：
  * `seg\HMM`，基于HMM模型的分词算法
  * `seg\algorithm`，viterbi算法
* 基于统计的词性标注算法：
  * `postagger\HMM`，预计HMM模型的词性标注算法
  * `postagger\algorithm`，viterbi算法
* 基于统计的命名实体识别算法：
  * `ner\HMM`，基于HMM模型的命名实体识别
  * `ner\algorithm`，viterbi算法
* 分词评测算法：
  * `evaluator\segEvaluator`
* 词性标注评测算法：
  * `evaluator\posEvaluator`



## 待完成

- [ ] 添加MM测试进度条
- [x] 添加命名实体识别评测算法
- [ ] 添加基于CRF的词性标注算法，及评测算法
- [ ] 添加基于CRF的命名实体算法，及评测算法
- [x] 检查当前评测算法
- [x] 撰写文档和报告





## data文件夹说明

* `ner-processed`：预处理后，用于命名实体识别的人民日报预料，处理程序见`tools\nerPreProcess.py`
  * `199801-test.txt`
  * `199801-train.txt`
* `pos-processed`：预处理后，用于词性标注的人民日报预料，处理程序见`tools\posPreProcess.py`
  * `199801-test.txt`
  * `199801-train.txt`
  * `tagSet.txt`：所有的标签文件
* `seg-processed`：预处理后，用于分词的微软语料库，处理程序见`tools\segPreProcess.py`
  * `msr_train.txt`
* `199801-test.txt` ：人民日报测试集，原数据，用于评测词性标注、命名实体识别
* `199801-train.txt`：人民日报训练集，原数据，用于训练词性标注、命名实体识别
* `199801.txt`：人民日报，原数据
* `dictionary.txt`：词典，[来源](https://github.com/0612800232/HanLP/blob/master/data/dictionary/CoreNatureDictionary.mini.txt)
* `msr_test.txt`：微软语料库，在本次项目中未使用
* `msr_train.txt`：微软语料库，用于训练分词，评测分词算法性能

