#coding:utf-8
#2017 04 29
#ding

#term frequency-inverse class frequency

#import
import math
from model.funcs import *
from model.classes import *


#testData
testLabelTrain = ['hack','weapon','porn']

testKeyExpert = dict()
testKeyExpert['hack'] = ['hacking','hacker','hacking']
testKeyExpert['weapon'] = ['weapon','gun']
testKeyExpert['porn'] = ['sex','girl']

testContentTrain = [ \
    doc(tokenize('gun'), tokenize('gun 1 2 3 4 hacking'),['hack','weapon']),\
    #doc(tokenize('gun'), tokenize('gun apple samsung google gun'),['weapon']),\
    #doc(tokenize('sex girl'),['happy','new','year','sex','girl'],['porn'])\
    ]

lamda = 1.0
#tf-icf
def tf_icfFeature(k_expert_id = [], c_train_id = [], c_train_m = [], c_train_label = []\
, l_train_sorted = [],len_dic = 0):

    #output M[class][word]
    M = np.array([[0.0 for w in xrange(len_dic)] \
     for topic in xrange(len(l_train_sorted))])

    #key in k_expert
    for topic in xrange(len(k_expert_id)):
        for key in set(k_expert_id[topic]):
            M[topic][key] += categoryCount(k_expert_id, key, topic)
    #print M

    for docID in xrange(len(c_train_id)):
        m = c_train_m[docID]
        if m <= 0:
            continue
        else:
            for c in c_train_label[docID]:
                M[c] += c_train_id[docID]/m
    #print M

    #compute tficf socres per class using M
    for w in xrange(len_dic):
        icfw = 0.0
        for c in xrange(len(l_train_sorted)):
            if M[c][w] > 0:
                icfw += 1
        if icfw > 0.0:
            icfw = math.log(float(len(l_train_sorted))/icfw)
        for c in xrange(len(l_train_sorted)):
            M[c][w] = M[c][w] * icfw

    return [M[c] for c in xrange(len(l_train_sorted)) if c in sum(c_train_label, [])],\
    [c for c in xrange(len(l_train_sorted)) if c in sum(c_train_label, [])]



#k_expert dict->list
#l_train_sorted, k_expert_list = dict2list(testKeyExpert,testLabelTrain)
#word to id
#dic, c_train_id, c_train_label, c_train_m, k_expert_id = word2ID(\
#k_expert_list, testContentTrain,l_train_sorted, lamda)

#M,L = tf_icfFeature(k_expert_id, c_train_id, c_train_m, c_train_label\
#,l_train_sorted,len(dic))
#print M,L