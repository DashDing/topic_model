#coding:utf-8
#2017 04 30
#ding

#import 
import numpy as np
from model.classes import doc
from model.funcs import *
from model.config import *
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from TFICF import tf_icfFeature


#testData

#input


#main
TOPN = 1
printKeyword = False
draw = False
makeSet = False
def classifier(TopKeywords = 0,c_train_label = dict(),c_test_label = dict(),threshold = 0.0):

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
    dic,M = dimReduce(dic,M,threshold)
    print len_dic
    len_dic = len(dic)
    print len_dic
    k_expert_id_updated = []
    '''
    temp= []
    for c in xrange(len(l_train_sorted)):
        if c in L and c == l_train_sorted.index('identity'):
            l_word = list(M[L.index(c)])
            temp = sorted(l_word, reverse=True)
            #temp = temp[0:300]
            print len(temp)

            keywords = []
            for weight in temp:
                if weight >0 :
                    k = l_word.index(weight)
                    keywords.append(k)
                    l_word[k] = 0
            k_expert_id_updated.append(keywords)
        else:
            k_expert_id_updated.append([])
    '''
    if printKeyword:
        #print k_expert_id_updated
        #for c in xrange(len(k_expert_id_updated)):
        c = l_train_sorted.index('identity')
        print l_train_sorted[c], ':\n'
        f = open('text.txt','w')
        #for k in xrange(len(k_expert_id_updated[c])):
        for k in xrange(len(temp)):
            try:
                f.write('{}\n'.format(temp[k]))
                #print ' {} {}'.format(id2word(dic,k_expert_id_updated[c][k]),temp[k])
            except:
                continue
                #print ' {}'.format(k_expert_id_updated[c][k])
        print '\n'
        return 0

    #tf-icf
    print 'train data -> tf-icf ...'
    d_train = []
    d_train_l = []
    c_train_files_id = [doc2id(doc, dic, l_train_sorted) for doc in c_train_files]
    for docu in xrange(len(c_train_m)):
        content = np.array([0.0 for w in xrange(len_dic)])
        for i in xrange(len(dic)):
            content[i] = c_train_files_id[docu].getContent().count(i)
        M, L = tf_icfFeature(k_expert_id_updated, [content], [c_train_m[docu]], \
                             [c_train_label[docu]], l_train_sorted, len_dic)
        d_train += M
        d_train_l += L

    #draw pic
    if draw == True:
        print 'draw pic ...'
        drawPic(d_train,d_train_l)
        return

    #init classifiers(naive bayes/ svm/ LogisticRegression)
    print 'init classifiers ...'
    ml = MultinomialNB()
    svm = SVC()
    lr = LogisticRegression()

    #train
    print 'train classfifers ...'
    ml.fit(d_train,d_train_l)
    svm.fit(d_train,d_train_l)
    lr.fit(d_train,d_train_l)

    #test
    print 'choice test file ...'
    c_test_files = readFiles(c_test_path, c_test_label)
    c_test_files_id = [doc2id(doc, dic, l_train_sorted) for doc in c_test_files]

    #score
    print 'testing ...'
    count = 0.0
    right = .0

    # predict_proba test
    for c_test_index in xrange(len(c_test_files_id)):
        count += 1
        content = []
        for i in xrange(len(dic)):
            content.append(c_test_files_id[c_test_index].getContent().count(i))
        labels = c_test_files_id[c_test_index].getLabels()
        temp_ml = ml.predict_proba([content])[0]
        predict_proba_result_ml = [score for score in temp_ml]
        topN = []
        tiao = False
        # nb
        score = 0.3
        temp = []
        while score >= 0.25:
            score = max(predict_proba_result_ml)
            index_ml = predict_proba_result_ml.index(score)
            predict_proba_result_ml[index_ml] = -1
            topN.append(index_ml)

        temp_svm = svm.predict([content])
        temp_lr = lr.predict_proba([content])[0]
        predict_proba_result_ml = [score for score in temp_ml]
        predict_proba_result_lr = [score for score in temp_lr]
        topN = []
        tiao = False
        #nb
        score = 0.3
        temp = []
        while score >= 0.25:
            score = max(predict_proba_result_ml)
            index_ml = predict_proba_result_ml.index(score)
            predict_proba_result_ml[index_ml] = -1
            temp.append(index_ml)
        #svm
        temp = temp + [temp_svm[0],]
        #lr
        score = 0.3
        while score >= 0.25:
            score = max(predict_proba_result_lr)
            index_lr = predict_proba_result_lr.index(score)
            predict_proba_result_lr[index_lr] = -1
            temp.append(index_lr)
        for x in xrange(len(temp)):
            topN.append(temp[x])
        for i in xrange(3):
            topN += [label for label in temp if temp.count(label) == i]
        topN = set(topN[0:3])

        #print predict_proba_result
        for c in topN:
            if c in labels:
                right +=1
                tiao = True
                break
        #if not tiao:
        #    print '{}-{}'.format([l_train_sorted[c] for c in topN],\
        #    [l_train_sorted[c] for c in labels])

    print 'test finished: score {}'.format(right/count)
    return right/count
    '''
    for c_test_index in xrange(len(c_test_files_id)):
        count += 1
        content,labels = normalize(c_test_files_id[c_test_index],len_dic)
        predict_result = ml.predict([content])
        #print l_train_sorted[predict_result[0]],',',l_train_sorted[labels[0]]
        #test_contents.append(content)
        #test_labels.append(labels)
        if int(predict_result) in labels:
            right +=1
        else:
            print '{}-{}'.format(l_train_sorted[int(predict_result)],[l_train_sorted[c] for c in labels])
    print 'NB model test finished: score {}'.format(right/count)
    #print 'test finished: score {}'.format(ml.score(test_contents,test_labels))
    return right/count
    '''
'''
    #predict
    #unlabeled docs
    c_unlabel_files = readUnlabelFiles(c_unlabel_path)
    c_unlabel_files_id = [[dic.get(w,-1) for w in file] for file in c_test_files]
    #predict
    for c_unlabel_index in xrange(c_unlabel_files_id):
        predict_result = ml.predict(c_unlabel_files_id[c_unlabel_index])
        prob = ml.predict_proba(c_unlabel_files_id[c_unlabel_index])
'''

def main(e):
    # shi ze jiao cha
    c_train_label = dict(c_train_label_default)
    l_train.sort()
    c_train_label_list = []

    if makeSet == True:
        # make 10 pieces train sets
        f = open('TrainSet.py', 'w')
        for x in xrange(10):
            temp = dict()
            count = 0
            count2 = 0
            for label in l_train:
                urls = [w for w in c_train_label if label in c_train_label[w]]
                num = len(urls) / (10 - x)
                count += num
                ids = []
                while num > 0 and len(ids) < num:
                    choice = random.randint(0, len(urls) - 1)
                    if choice not in ids:
                        ids.append(choice)
                count2 += len(ids)
                for i in ids:
                    url = urls[i]
                    temp[url] = c_train_label[url]
                    del c_train_label[url]
            f.write('temp{}='.format(x))
            f.write('{')
            for l in temp:
                f.write('"{}":["{}"],\n'.format(l, '","'.join(temp[l])))
            f.write('}\n')
            c_train_label_list.append(temp)
        f.write(
            'def get_c_train_label_list():\n    return [temp0, temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9]')
    else:
        from TrainSet import get_c_train_label_list
        c_train_label_list = get_c_train_label_list()
    nb = []

    # j means the test set
    for j in xrange(10):
        c_t = dict()
        for i in xrange(10):
            if not i == j:
                for k in c_train_label_list[i]:
                    c_t[k] = c_train_label_list[i][k]
        c_test = c_train_label_list[j]
        print len(c_test)
        a = classifier(10, c_train_label=c_t, c_test_label=c_test,threshold=e)
        nb.append(a)

    print 'NB:{}\n'.format(nb)

if __name__ == '__main__':
    for i in xrange(10):
        main(i/100.0)