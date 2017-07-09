#encoding:utf-8
import numpy as np
from hmmlearn import hmm
from random import random
class hmm_test:

    def __init__(self,start_prob,trans_matrix,M):
        self.start_prob = start_prob
        self.trans_matrix = trans_matrix
        self.M = M
        self.N = len(self.start_prob)
        self.d = len(self.M[0])

    def predict(self,content_bow):
        #result
        result = []

        #choose start status
        current_status = self.choice_start_status()
        #result.append(current_status)

        #predict
        #for every word
        for i in xrange(len(content_bow)):
            current_prob = self.trans_matrix[current_status]
            current_result = []
            #for evey label
            for j in xrange(self.N):
                current_result.append(current_prob[j]*self.M[j][i])
            max_prob = max(current_result)
            current_status = current_result.index(max_prob)
            result.append(current_status)

        return result

    #def learn_trans(self,xs,labels):
    #    for i in xrange(len(labels)):

    def normalize(self):
        sum_start = sum(self.start_prob)
        for i in xrange(self.N):
            self.start_prob[i] = float(self.start_prob[i])/sum_start

        for i in xrange(self.N):
            sum_label = sum(self.M[i])
            for j in xrange(self.d):
                self.M[i][j] = self.M[i][j]/sum_label

        for i in xrange(self.N):
            sum_trans = sum(self.trans_matrix[i])
            for j in xrange(self.N):
                self.trans_matrix[i][j] = float(self.trans_matrix[i][j])/sum_trans

    def choice_start_status(self):
        choice_prob = random()
        choice = 0
        for i in xrange(self.N):
            if choice_prob > self.start_prob[i]:
                choice_prob -= self.start_prob[i]
            else:
                choice = i
                break
        return choice

if __name__ == '__main__':
    #test
    M = [[1.0,0.,0.],[0.0,1.,0.0]]
    trans = [[0.5,0.5],[0.5,0.5]]
    s = [0.3,0.7]
    x = [0,0,1,0,1]
    #hmm_test(M,)
    a = hmm_test(s,trans,M)
    print a.predict(x)

