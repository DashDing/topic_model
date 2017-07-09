#coding:utf-8
#2017 04 30
#ding

#import 
import numpy as np
from model.classes import doc
from model.funcs import *
from model.config import *
from TFICF import tf_icfFeature

#testData

#input

#main
TOPN = 1
printKeyword = False
draw = False
makeSet = False
def classifier(TopKeywords = 0,c_train_label = dict(),c_test_label = dict()):

    #train
    #read train data
    print 'read c_train data from file ...'
    c_train_files = readFiles(c_train_path, c_train_label)
    #k_expert dict->list
    print 'l_train sort and k_expert list ...'
    l_train_sorted, k_expert_list = dict2list(k_expert,l_train)
    #word to id
    print 'c_train init, make dic ...'
    dic, c_train_id, c_train_label, c_train_m, k_expert_id = word2ID( \
    k_expert_list, c_train_files,l_train_sorted, lamda)
    len_dic = len(dic)

    #find keywords()
    print 'find keywords from train set ...'
    M,L = tf_icfFeature(k_expert_id, c_train_id, c_train_m, \
        c_train_label, l_train_sorted, len_dic)
    k_expert_id_updated = []

    #init hmm
    print 'hmm_test ...'
    from hmm_test import hmm_test
    #cal start prob
    start_prob = []
    #cal trans matrix
    trans_matrix = []
    for i in xrange(len(l_train_sorted)):
        temp = [c_train_label[c] for c in xrange(len(c_train_label)) if i in c_train_label[c]]
        start_prob.append(len(temp))
        sum_temp = sum(temp,[])
        trans_temp = []
        for j in xrange(len(l_train_sorted)):
            if sum_temp.count(j) > 0:
                trans_temp.append(sum_temp.count(j))
            else:
                trans_temp.append(1)
        trans_matrix.append(trans_temp)

    hmm = hmm_test(start_prob,trans_matrix,M)
    #test
    choice = random.randint(0,len(c_train_label))
    x = c_train_files[choice].getContent()
    print x
    x = ver(dic,x)
    print x
    result = [c_train_label[choice]]
    hmm.normalize()
    pre_result = hmm.predict(x)
    #drawPic([pre_result],[1])
    print 'pre_result:',pre_result
    print 'result',result






def ver(dic,content):
    content_list = []
    for i in xrange(len(content)):
        if content[i] in dic:
            content_list.append(dic[content[i]])
    return content_list


if __name__ == '__main__':

    # shi ze jiao cha
    c_train_label = dict(c_train_label_default)
    l_train.sort()

    from TrainSet import get_c_train_label_list
    c_train_label_list = get_c_train_label_list()
    nb = []
    hmm_test_set = dict()
    #j means the test set:
    c_t = dict()
    for i in xrange(10):
        if i == 4:
            for k in c_train_label_list[i]:
                hmm_test_set[k] = c_train_label_list[i][k]
        if not i == -1:
            for k in c_train_label_list[i]:
                c_t[k] = c_train_label_list[i][k]

    a = classifier(10,c_train_label=c_t)
    nb.append(a)
    print 'NB:{}\n'.format(nb)