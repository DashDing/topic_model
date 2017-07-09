#coding:utf-8
#2017 04 30
#ding

#import 

import os
import re
from collections import OrderedDict
import chardet
import nltk
import hashlib
import random
import numpy as np
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from additionalStopWords import AdditionalStopWord
from classes import doc
from config import *
from random import choice

stopwords = stopwords.words('english')

#random_product_c_test_label
def randomProductC_test_label(c_train_label = c_train_label_default):

    c_test_label = dict()
    for label in l_train:
        num = 3
        urls = [w for w in c_train_label if label in c_train_label[w]]
        ids = []
        for i in xrange(num):
            choice = random.randint(0,len(urls)-1)
            if choice not in ids:
                ids.append(choice)
        for i in ids:
            url = urls[i]
            c_test_label[url] = c_train_label[url]

    return c_test_label
        
        

#detect encoding
def detectStrEncoding(str):
    encoding = chardet.detect(str).get('encoding')
    if encoding is None:
        encoding = 'utf-8'
    return encoding

def doc2id(doc_t, dic, l_train):
    new_title = []
    new_content = []
    new_label = []
    for w in doc_t.getTitle():
        if w in dic:
            new_title.append(dic[w])
    for w in doc_t.getContent():
        if w in dic:
            new_content.append(dic[w])
    for w in doc_t.getLabels():
        if w in l_train:
            new_label.append(l_train.index(w))
    return doc(new_title, new_content, new_label)

def normalize(doc_id,len_dic):
    content = doc_id.getContent()
    newcontent = np.array([0.0 for index in xrange(len_dic)])
    for w in content:
        newcontent[w] += 1
    del content
    return newcontent,doc_id.getLabels()

def readUnlabelFiles(c_path):
    if os.path.isdir(c_path):
        output = []
        for root, dirs, files in os.walk(c_path):
            for name in files:
                #read file content
                f = open(os.path.join(c_path,name),'r')
                page_content = f.read()
                f.close() 
                #coding -> utf8
                code = detectStrEncoding(page_content)
                page_content_utf8 = page_content.decode(code).encode('UTF-8')
                #grep filter
                for r in deleteGroup:
                    page_content_utf8 = re.compile(r).sub(' ',page_content_utf8)
                #text -> doc
                soup = BeautifulSoup(page_content_utf8, 'lxml')
                #remove symbol
                content_utf8_main = re.complie(deleteSymbol).sub(' ',soup.get_text())
                output.append(tokenize(content_utf8_main.lower()))
        return ouput
    else:
        return None

def url2filename(url):
    filename = hashlib.md5(bytes(url.encode('utf8'))).hexdigest()+'default.html'
    return filename

#read all file from a folder
def readFiles(c_path,c_labels):

    #is exist?
    if os.path.isdir(c_path):

        #output
        output = []
        count = 0
        for url in c_labels:
            file = url2filename(url) 
            if os.path.exists(c_path+file):

                #count
                #print 'deal with : ',count,' ',file
                count += 1
                #read file content
                f = open(os.path.join(c_path,file),'r')
                page_content = f.read()
                f.close() 
                #coding -> utf8
                code = detectStrEncoding(page_content)
                page_content_utf8 = page_content.decode(code).encode('utf-8')
                #grep filter
                for r in deleteGroup:
                    page_content_utf8 = re.compile(r).sub(' ',page_content_utf8)
                #text -> doc
                soup = BeautifulSoup(page_content_utf8, 'lxml')
                title_str = soup.title.string if soup.title is not None and soup.title.string is not None else ''
                content_str = soup.get_text() if soup.get_text() is not None else ''
                title_str = re.compile(deleteSymbol).sub(' ',title_str)
                content_str = re.compile(deleteSymbol).sub(' ',content_str)
                title = tokenize(title_str.lower())
                content = tokenize(content_str.lower())
                labels = c_labels[url]
                output.append(doc(title,content,labels))
                del soup
        return output
    else:
        return None

#tokenize
#needed nltk words tag
tagIcon = ['NN','NNS','VB','VND','VBG','VBN','VBP','VBX']
from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()
def tokenize(str):
    output = []
    words = []
    sens = nltk.sent_tokenize(str)
    for sent in sens:
        for word in nltk.word_tokenize(sent):
            words.append(st.stem(word))
            #words.append(word)
    tags = nltk.pos_tag(words)
    for (word, tag) in tags:
        if tag in tagIcon:
            output.append(word)
    return [w for w in output if \
    (not w in stopwords and not w in AdditionalStopWord and len(w) >2)]

#word to id
def word2ID(k_expert, c_train, l_train, lamda):

    #local value
    word2idIndex = 0

    #return value
    word2id = OrderedDict()
    k_expert_id = []
    c_train_id = []
    c_train_label_id = []
    c_train_m = []

    #k_expert_id
    for topic in xrange(len(k_expert)):
        topic_key = []
        for key in xrange(len(k_expert[topic])):
            if k_expert[topic][key] in word2id:
                topic_key.append(word2id[k_expert[topic][key]])
            else:
                word2id[k_expert[topic][key]] = word2idIndex
                topic_key.append(word2idIndex)
                word2idIndex += 1
        k_expert_id.append(topic_key)

    #dic
    for docID in xrange(len(c_train)):
        content = c_train[docID].getContent()
        for w in content:
            if w not in word2id:
                word2id[w] = word2idIndex
                word2idIndex += 1
        title = c_train[docID].getTitle()
        for w in title:
            if w not in word2id:
                word2id[w] = word2idIndex
                word2idIndex += 1
    #c_train_id
    for docID in xrange(len(c_train)):
        title, content, labels = c_train[docID].getAll()
        newcontent = np.array([0.0 for index in xrange(word2idIndex)])
        newlabels = []
        newm = len(content)
        for w in title:
            newcontent[word2id[w]] += 1.0*lamda

        for w in content:
            newcontent[word2id[w]] += 1.0

        for c in labels:
            newlabels.append(l_train.index(c))
        
        c_train_id.append(newcontent)
        c_train_label_id.append(newlabels)
        c_train_m.append(newm)

    return word2id, c_train_id, c_train_label_id, c_train_m, k_expert_id

def categoryCount(k_expert_list, k, c):
    return len([w for w in k_expert_list[c] if w == k])

def onionCount(w, d):
    return len([word for word in d if word == w ])

#topic-key dict->list
def dict2list(dic, classList):
    #output 
    keyList = []
    classList.sort()

    for topicID in xrange(len(classList)):
        keys = dic.get(classList[topicID],None)
        if not keys is None:
            keyList.append(keys)
        else:
            keyList.append([])
    return classList,keyList

#id-word
def id2word(dic,word):
    return OrderedDict({value:key for key,value in dic.items()})[word]

#drawpic
def drawPic(data, data_label):
    import matplotlib.pyplot as plt
    from matplotlib.colors import cnames
    plt.figure(figsize=(8, 8))
    for i in xrange(len(data)):
        color = data_label[i]
        count = 0
        for j in cnames:
            if count == color:
                plt.plot(range(len(data[i])), data[i], j)
            count += 1
    plt.savefig('all_samples.svg')
    plt.show()
