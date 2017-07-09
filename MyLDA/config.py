#coding:utf-8
#2017 04 23
#ding

#Config

#Default Value
# topic number
DefaultK = 1
# alpha
DefaultAlpha = 1.0/DefaultK
# beta
DefaultBeta = DefaultAlpha
# iter times
DefaultIterTimes = 1000
# top words
DefaultTopWords = 10

#needed nltk words tag
tagIcon = ['NN','NNS','VB','VND','VBG','VBN','VBP','VBX']

#path
import os
path = os.path.abspath('.')

#word2id file
word2idFilename = 'word2id.py'
#matrix file
matrixFilename = 'matrix.py'
#settings file
settingsFilename = 'settings.py'
#topic's keywords
topNFilename = 'topN.txt'
#doc-word-topic result file
tassginFilename = 'tassgin.txt'
