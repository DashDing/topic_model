#coding:utf-8
#2017 04 26
#ding

#some tool functions


# -*- coding:utf-8 -*-
#2017 03 24 ding
#jssec

import nltk
from nltk.corpus import stopwords
from StopWord import myStopWord
stopwords = stopwords.words('english')
tagIcon = ['NN','NNS','VB','VND','VBG','VBN','VBP','VBX']
def tokenize(str):
    output = []
    words = []
    sens = nltk.sent_tokenize(str)
    for sent in sens:
        for word in nltk.word_tokenize(sent):
            words.append(word)
    tags = nltk.pos_tag(words)
    for (word, tag) in tags:
        if tag in tagIcon:
            output.append(word)
    return [w for w in output if (not w in stopwords and not w in myStopWord and len(w)>2)]

def print_top_words(model, feature_names, n_top_words):
    outputs = ''
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        outputs += message+'\n'
    return outputs

def predict(model,words,feature_names):
    phi = model.components_
    topicList = []
    for topic_idx, topic in enumerate(model.components_):
        score = 0.0
        for wordIndex in words:
            score += topic[wordIndex]
        if score > 0.0:
            topicList.append([topic_idx,score])
    return sorted(topicList, key = lambda x:x[1])

def str2word2id(dic,str):
    words = tokenize(str)
    ids = [dic.index(word) for word in words if word in dic]
    return ids

