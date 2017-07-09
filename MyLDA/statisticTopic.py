#coding:utf-8
#2017 04 24
#ding

#import
from func import tokenize,preprocessing
from lda import LDAModel

#main
if __name__ == '__main__':
    
    #files -> bow
    trainSet = [['1','2','3','4','5'],\
    ['apple','samsung','google','baidu'],\
    ['happy','new','year','1']]

    #lda
    pre = preprocessing(trainSet)
    lda = LDAModel(k = 10,preProcessing = pre,iterTimes = 1000)
    lda.estimate()
    lda.save()
