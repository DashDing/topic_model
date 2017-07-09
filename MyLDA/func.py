#coding:utf-8
#2017 04 23
#ding

#Functions

import random
import nltk
from config import *
from classes import *
from nltk.corpus import stopwords
from additionalStopWords import AdditionalStopWord
from nltk.stem.lancaster import LancasterStemmer
stopwords = stopwords.words('english')
#random topic
def randomTopic(k = DefaultK):
    return random.randint(0,k-1)

#tokenize
def tokenize(str):
    output = []
    words = []
    sens = nltk.sent_tokenize(str)
    for sent in sens:
        for word in nltk.word_tokenize(sent):
            #words.append(st.stem(word))
            words.append(word)
    tags = nltk.pos_tag(words)
    for (word, tag) in tags:
        if tag in tagIcon:
            output.append(word)
    return [w for w in output if \
    (not w in stopwords and not w in AdditionalStopWord)]

#preprocessing
def preprocessing(trainedFile):
        
        #pre processing function
        print 'pre processing'
        pre = PreProcessing()
        docs = trainedFile
        wordId = 0
        for doc in docs:
            if len(doc) > 0:
                temp = Document()
                for word in doc:
                    if pre.word2id.has_key(word):
                        temp.words.append(pre.word2id[word])
                    else:
                        pre.word2id[word] = wordId
                        temp.words.append(wordId)
                        wordId += 1
                temp.length = len(doc)
                pre.docs.append(temp)
            else:
                continue
        pre.docsCount = len(pre.docs)
        pre.wordsCount = len(pre.word2id)
        
        print 'pre processing finished'
        #print some statistic value
        print 'some statistic value:\n'
        print 'total docs: {}'.format(pre.docsCount)
        print 'total words: {}'.format(pre.wordsCount)

        return pre
