#coding:utf-8
#2017 04 30
#ding

#import
import numpy as np
from model.classes import doc
from model.funcs import *
from model.config import *
from TFICF import tf_icfFeature
from hashes.simhash import simhash
import math
#main
cal = True

def cos_corrcoef(A,B):
    if len(A)!=len(B):
        return 0
    m_A = .0
    m_B = .0
    result = .0
    for i in xrange(len(A)):
        m_A += math.pow(A[i],2)
        m_B += math.pow(B[i],2)
        result += A[i] * B[i]
    return result/(math.sqrt(m_A)*math.sqrt(m_B))

def simple_common_word(A,B):
    l_A = 0
    l_B = 0
    common_words = 0
    for i in xrange(len(A)):
        if A[i] > 0 and B[i] > 0:
            common_words += 1
        if A[i] > 0:
            l_A += 1
        if B[i] > 0:
            l_B += 1
    return float(common_words)/max(l_A,l_B)

def jaccard_corrcoef(A,B):
    l = 0
    common_words = 0
    for i in xrange(len(A)):
        if A[i] > 0 and B[i] > 0:
            common_words += 1
        if A[i] > 0 or B[i] > 0:
            l += 1
    return float(common_words) / l

def Euclid_corrcoef(A,B):
    #Euclid_distance
    d_euclid = 0
    for i in xrange(len(A)):
        d_euclid += (A[i]-B[i])*(A[i]-B[i])
    return 1/(math.sqrt(d_euclid)+1)

def Manhattan_corrcoef(A,B):
    #manhattan_distance
    d_manhattan = 0
    for i in xrange(len(A)):
        d_manhattan += math.fabs(A[i]-B[i])
    return float(1)/(d_manhattan+1)

def simhash_hamming_corrcoef(A,B):
    str_A = []
    str_B = []
    for i in xrange(len(A)):
        str_A.append(str(A[i]))
        str_B.append(str(B[i]))
    hash_A = simhash(','.join(str_A))
    hash_B = simhash(','.join(str_B))
    return hash_A.similarity(hash_B)




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
    print 'tficf ...'
    M,L = tf_icfFeature(k_expert_id, c_train_id, c_train_m, \
        c_train_label, l_train_sorted, len_dic)
    k_expert_id_updated = []

    #cos_corrcoef
    words_str = "["
    cos_str = "["
    jaccard_str = "["
    euclid_str = "["
    manhattan_str = "["
    simhash_hamming_str = '['
    for i in xrange(len(M)):
        words_temp = []
        cos_temp = []
        jaccard_temp = []
        euclid_temp = []
        manhattan_temp = []
        simhash_hamming_temp = []

        for j in xrange(len(M)):
            cos_result = cos_corrcoef(M[i],M[j])
            words_result = simple_common_word(M[i],M[j])
            jaccard_result = jaccard_corrcoef(M[i],M[j])
            euclid_result = Euclid_corrcoef(M[i],M[j])
            manhattan_result = Manhattan_corrcoef(M[i],M[j])
            simhash_hamming_result = simhash_hamming_corrcoef(M[i],M[j])

            words_temp.append(str(words_result))
            cos_temp.append(str(cos_result))
            euclid_temp.append(str(euclid_result))
            jaccard_temp.append(str(jaccard_result))
            manhattan_temp.append(str(manhattan_result))
            simhash_hamming_temp.append((str(simhash_hamming_result)))

        words_str += "[{}],".format(','.join(words_temp))
        cos_str += "[{}],".format(','.join(cos_temp))
        jaccard_str += "[{}],".format(','.join(jaccard_temp))
        euclid_str += "[{}],".format(','.join(euclid_temp))
        manhattan_str += "[{}],".format(','.join(manhattan_temp))
        simhash_hamming_str += '[{}],'.format(','.join(simhash_hamming_temp))
    words_str += "]"
    cos_str += "]"
    jaccard_str += "]"
    euclid_str += "]"
    manhattan_str += "]"
    simhash_hamming_str += ']'
    f = open('corrcoef_matrix.py','w')
    f.write('word_corrcoef_matrix = {}\n\n'.format(words_str))
    f.write('cos_corrcoef_matrix = {}\n\n'.format(cos_str))
    f.write('jaccard_corrcoef_matrix = {}\n\n'.format(jaccard_str))
    f.write('euclid_corrcoef_matrix = {}\n\n'.format(euclid_str))
    f.write('manhattan_corrcoef_matrix = {}\n\n'.format(manhattan_str))
    f.write('simhash_hamming_corrcoef_matrix = {}\n\n'.format(simhash_hamming_str))
    f.close()



    #

    return 1

if __name__ == '__main__':

    if cal == True:
        # shi ze jiao cha
        c_train_label = dict(c_train_label_default)
        l_train.sort()
        from TrainSet import get_c_train_label_list
        c_train_label_list = get_c_train_label_list()
        nb = []
        c_t = dict()
        for i in xrange(10):
            for k in c_train_label_list[i]:
                c_t[k] = c_train_label_list[i][k]
        a = classifier(10,c_train_label=c_t)
    else:
        from corrcoef_matrix import word_corrcoef_matrix
        from corrcoef_matrix import cos_corrcoef_matrix
        from corrcoef_matrix import jaccard_corrcoef_matrix
        from corrcoef_matrix import euclid_corrcoef_matrix
        from corrcoef_matrix import simhash_hamming_corrcoef_matrix
        from corrcoef_matrix import word_corrcoef_matrix

        #if