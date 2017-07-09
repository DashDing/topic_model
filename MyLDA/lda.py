#coding:utf-8
#2017 04 23
#ding

from config import *
from func import *
from classes import *
import numpy as np

#LDAModel
class LDAModel:
    
    #init function
    def __init__(self,k = DefaultK, alpha = DefaultAlpha
    , beta = DefaultBeta, iterTimes = DefaultIterTimes
    , topWords = DefaultTopWords, preProcessing = PreProcessing()):

        self.preProcessing = preProcessing

        # init value
        # topic number
        self.k = int(k)
        # alpha
        self.alpha = float(alpha)
        # beta
        self.beta = float(beta)
        # iter times
        self.iterTimes = int(iterTimes)
        # top words
        self.topWords = int(topWords)

        # init 
        #self.wordidmapfile = 
        #self.trainedFile = trainedFile
        #self.theta = theta
        #self.phifile = phi
        #self.topN = topN
        
        #init matrix
        self.p = np.zeros(self.k)
        #word-topic
        self.nw = np.zeros((self.preProcessing.wordsCount,self.k), dtype=int)
        #per topic's total words
        self.nwsum = np.zeros(self.k, dtype=int)
        #doc-topic
        self.nd = np.zeros((self.preProcessing.docsCount,self.k), dtype=int)
        #per doc's total words
        self.ndsum = np.zeros(self.preProcessing.docsCount, dtype = int)
        #doc-word's topic
        self.z = np.array([[0 for wordIndex in xrange(self.preProcessing.docs[doc].length)]\
            for doc in xrange(self.preProcessing.docsCount)])
        #theta
        self.theta = np.array([[ 0.0 for topic in xrange(self.k)] \
         for doc in xrange(self.preProcessing.docsCount)])
        #phi
        self.phi = np.array([[ 0.0 for word in xrange(self.preProcessing.wordsCount)] \
         for topic in xrange(self.k)])

        #random topic product
        for docIndex in xrange(len(self.z)):
            self.ndsum[docIndex] = self.preProcessing.docs[docIndex].length
            for wordIndex in xrange(self.preProcessing.docs[docIndex].length):
                topic = randomTopic(self.k)
                self.z[docIndex][wordIndex] = topic
                self.nw[self.preProcessing.docs[docIndex].words[wordIndex]][topic] += 1
                self.nd[docIndex][topic] += 1
                self.nwsum[topic] += 1

    def load(self):
        from matrix import theta, phi, nw, nwsum, nd, ndsum, p, z
        from settings import k,alpha,topWords,beta,topWords
        self.k = k
        self.alpha = alpha
        self.beta = beta
        self.iterTimes = iterTimes
        self.topWords = topWords
        self.theta = theta
        self.phi = phi
        self.nw = nw
        self.nwsum = nwsum
        self.nd = nd
        self.ndsum = ndsum
        self.p = p
        self.z = z

    #gibbs sampling
    def sampling(self,docIndex,wordIndex):

        #topic and word
        topic = self.z[docIndex][wordIndex]
        word = self.preProcessing.docs[docIndex].words[wordIndex]

        #decrease
        self.nw[word][topic] -= 1
        self.nd[docIndex][topic] -= 1
        self.nwsum[topic] -= 1
        self.ndsum[docIndex] -= 1

        #p[topic]
        Vbeta = self.preProcessing.wordsCount * self.beta
        Kalpha = self.k * self.alpha
        self.p = (self.nw[word] + self.beta)/(self.nwsum + Vbeta) *\
                 (self.nd[docIndex] + self.alpha)/(self.ndsum[docIndex] + Kalpha)
        #newtopic
        newTopic = topic
        for topicIndex in xrange(self.k-1):
            self.p[topicIndex +1] += self.p[topicIndex]
        u = random.uniform(0,self.p[self.k-1])
        for topicIndex in xrange(self.k):
            if self.p[topicIndex] > u:
                newTopic = topicIndex
                break

        #increase
        self.nw[word][newTopic] += 1
        self.nd[docIndex][newTopic] += 1
        self.nwsum[newTopic] += 1
        self.ndsum[docIndex] += 1

        return newTopic
    
    #estimate func
    def estimate(self):
        #iteration
        for times in xrange(self.iterTimes):
            for docIndex in xrange(self.preProcessing.docsCount):
                for wordIndex in xrange(self.preProcessing.docs[docIndex].length):
                    topic = self.sampling(docIndex,wordIndex)
                    self.z[docIndex][wordIndex] = topic
        print 'estimate function ran'
        #theta
        for docIndex in xrange(self.preProcessing.docsCount):
            self.theta[docIndex] = (self.nd[docIndex] + self.alpha)/ \
            (self.ndsum[docIndex] + self.k * self.alpha)
        #phi
        for topicIndex in xrange(self.k):
            self.phi[topicIndex] = (self.nw.T[topicIndex] + self.beta)/ \
            (self.nwsum[topicIndex] + self.preProcessing.wordsCount * self.beta)
        #save

    #print topic's keywords
    def printTopic(self,topic):
        self.topWords = min(self.topWords, self.preProcessing.wordsCount)
        if topic > self.topWords:
            print 'topic ID is too large'
            return
        twords = []
        twords = [(wordIndex,self.phi[topic][wordIndex]) for wordIndex in xrange(self.preProcessing.wordsCount)]
        twords.sort(key = lambda x:x[1],reverse = True)
        output = '{}'
        for index in xrange(self.topWords):
            word = OrderedDict({value:key for key,value in self.preProcessing.word2id.items()})[twords[index][0]]
            output = output.format('{}:{} {}'.format(word,twords[index][1],'{}'))
        return output.format('\n')

    #save function
    def save(self):

        print 'save model'
        #save theta
        f = open(os.path.join(path, matrixFilename),'w')
        thetaTemp = []
        for doc in xrange(self.preProcessing.docsCount):
            line = ''
            for topic in xrange(self.k):
                line += str(self.theta[doc][topic])+','
            line = line[0:len(line) -1]
            thetaTemp.append(line)
        f.write('theta = [[{}]]\n'.format('],\n['.join(thetaTemp)))
        f.close()
        #save phi
        f = open(os.path.join(path, matrixFilename),'a')
        phiTemp = []
        for topic in xrange(self.k):
            line = ''
            for word in xrange(self.preProcessing.wordsCount):
                line += str(self.phi[topic][word])+','
            line = line[0:len(line) -1]
            phiTemp.append(line)
        f.write('phi = [[{}]]\n'.format('],\n['.join(phiTemp)))
        f.close()
        #save settings
        f = open(os.path.join(path, settingsFilename),'w')
        f.write('k = {}\n'.format(self.k))
        f.write('alpha = {}\n'.format(self.alpha))
        f.write('beta = {}\n'.format(self.beta))
        f.write('iterTimes = {}\n'.format(self.iterTimes))
        f.write('topWords = {}\n'.format(self.topWords))
        #save keywords
        f = open(os.path.join(path, topNFilename),'w')
        self.topWords = min(self.topWords, self.preProcessing.wordsCount)
        for topic in xrange(self.k):
            f.write('topic{} , {}'.format(topic, self.printTopic(topic)))
        f.close()
        #save doc-word-topic
        f = open(os.path.join(path, tassginFilename),'w')
        for doc in xrange(self.preProcessing.docsCount):
            for word in xrange(self.preProcessing.docs[doc].length):
                f.write(str(self.preProcessing.docs[doc].words[word]) + ':' \
                + str(self.z[doc][word]) + '\t')
            f.write('\n')
        f.close()
        #save z
        f = open(os.path.join(path, matrixFilename),'a')
        ztemp = []
        for doc in xrange(self.preProcessing.docsCount):
            line = ''
            for word in xrange(self.preProcessing.docs[doc].length):
                line += str(self.z[doc][word])+','
            line = line[0:len(line)-1]
            ztemp.append(line)
        f.write('z = [[{}]]\n'.format('],\n['.join(ztemp)))
        #f.close()
        pStr = ''
        for topic in xrange(self.k):
            pStr += str(self.p[topic])+','
        f.write('p = [{}]\n'.format(pStr[0:len(pStr)-1]))
        
        #word-topic
        nwtemp = []
        for word in xrange(self.preProcessing.wordsCount):
            line = ''
            for topic in xrange(self.k):
                line += str(self.nw[word][topic])+','
            line = line[0:len(line)-1]
            nwtemp.append(line)
        f.write('nw = [[{}]]\n'.format('],\n['.join(nwtemp)))

        nwsumStr = ''
        for topic in xrange(self.k):
            nwsumStr += str(self.nwsum[topic])+','
        f.write('nwsum = [{}]\n'.format(nwsumStr[0:len(nwsumStr)-1]))
        #doc-topic
        
        ndtemp = []
        for doc in xrange(self.preProcessing.docsCount):
            line = ''
            for topic in xrange(self.k):
                line += str(self.nd[doc][topic])+','
            line = line[0:len(line)-1]
            ndtemp.append(line)
        f.write('nd = [[{}]]\n'.format('],\n['.join(ndtemp)))

        #per doc's total words
        ndsumStr = ''
        for doc in xrange(self.preProcessing.docsCount):
            ndsumStr += str(self.ndsum[doc])+','
        f.write('ndsum = [{}]\n'.format(ndsumStr[0:len(ndsumStr)-1]))
        f.close()

        self.preProcessing.cachewordidmap()
        #save finished