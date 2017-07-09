#encoding:utf-8

#2017 05 30
#ding
#jssec

#import
from math import log

#class
class NaiveBayes:
    
    #init
    def __init__(self,lamda = 1.0):
        self.lamda = lamda

    def loadDataset(self,trainlist,labellist):
        self.trainset = [[int(p) for p in doc] for doc in trainlist]
        self.labelset = labellist

    def train(self):
        dataNum = len(self.trainset)
        feature = len(self.trainset[0])
        labels = list(set(self.labelset))
        labels.sort()
        self.d = feature
        self.K = len(labels)
        self.py = []
        self.sy = []
        for index in xrange(self.K):
            sy_c = len([1 for w in self.labelset if w == labels[index]])
            self.sy.append(sy_c)
            self.py.append((float(sy_c)+self.lamda)/(dataNum+self.K*self.lamda))
        #print self.sy

        self.statisticmatrix = []
        self.S = []
        self.matrix = []

        for d in xrange(feature):
            seenSet = set()
            for index in xrange(dataNum):
                if not self.trainset[index][d] in seenSet:
                    seenSet.add(self.trainset[index][d])
            
            
            temp1 = []
            temp2 = []
            for label in xrange(self.K):
                matrix_output = dict()
                output = dict()
                for count in seenSet:
                    sx_ay_c = len([1 for index in xrange(dataNum) if self.trainset[index][d] == count\
                    and self.labelset[index] == labels[label]])
                    output[str(count)] = sx_ay_c
                    px_ay_c = (float(sx_ay_c) + self.lamda)/(self.sy[label] + len(seenSet)*self.lamda)
                    matrix_output[str(count)] = px_ay_c
                temp1.append(output)
                temp2.append(matrix_output)
            self.statisticmatrix.append(temp1)
            self.matrix.append(temp2)
            self.S.append(len(seenSet))
        #print self.matrix

    def predict_log(self,doc):
        predict_result = []
        for i in xrange(self.K):
            p = log(self.py[i])
            for j in xrange(self.d):
                p += log(self.getNearest(self.matrix[j][i],doc[j]))
            predict_result.append(p)
        return predict_result

    def predict(self,doc):
        predict_result = []
        for i in xrange(self.K):
            p = self.py[i]
            for j in xrange(self.d):
                p *= self.getNearest(self.matrix[j][i],doc[j])
            predict_result.append(p)
        print predict_result
        s = sum(predict_result)
        print s
        for i in xrange(self.K):
            predict_result[i] = predict_result[i]/s
        return predict_result

    def getNearest(self,dic,key):
        minimum = 10000
        k = '0'
        for i in dic:
            index = int(i)
            if key == index:
                return dic[i]
            if abs(index-key) < minimum:
                minimum = abs(index-key)
                k = i
        return dic[k]

#test
t = [[1,4],[1,5],[1,5],[1,4],[1,4],[2,4],[2,5],[2,5],[2,6],[2,6],[3,6],[3,5],[3,5],[3,6],[3,6]]
l = [-1,-1,1,1,-1,-1,-1,1,1,1,1,1,1,1,-1]
nb = NaiveBayes()
nb.loadDataset(t,l)
nb.train()
print nb.predict([2,4])

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()
clf.fit(t,l)
print clf.predict_proba([[2,4]])