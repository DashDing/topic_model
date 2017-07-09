#coding:utf-8
#2017 04 23
#ding

#classes

from config import *

#Document
class Document(object):
    def __init__(self):
        self.words = []
        self.length = 0

#data pre processing
from collections import OrderedDict
class PreProcessing(object):
    def __init__(self):
        self.docsCount = 0
        self.wordsCount = 0
        self.docs = []
        self.word2id = OrderedDict()
    
    def cachewordidmap(self):
        #with codecs.open(wordidmapfile, 'w','utf-8') as f:
        f = open(os.path.join(path, word2idFilename),'w')
        f.write('from collections import OrderedDict\n')
        wordstemp = []
        for word,id in self.word2id.items():
            wordstemp.append("('{}',{})".format(word,id))
        f.write("word2id = OrderedDict([{}])".format(','.join(wordstemp)))
        f.close()