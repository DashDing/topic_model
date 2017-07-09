#coding:utf-8
#ding

#import
import os
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from funcs import print_top_words, tokenize, predict, str2word2id

#testdata
test_data_set = ['guns guns i have guns do you want one',\
    'i love you , i really love you',\
    'today, i go out to the market,i buy lots things. i will go to this market next sunday.']

#main
if __name__ == '__main__':

    #loading
    print 'loading dataset...'
    count = 0
    dataset = [] 
    walk = os.walk('/home/ding/Desktop/topic_resource/')
    for root, dirs, files in walk:
        for name in files:
            count += 1
            print count,'__count'
            f = open(os.path.join(root, name), 'r')
            raw = f.read().decode('utf8')
            dataset.append(raw)
            if count == 10000:
                break

    #tf-idf
    print 'tf-idf...'
    tfidf_verctorizer = TfidfVectorizer(stop_words='english',analyzer='word',max_df=0.95,\
    min_df=1,tokenizer=tokenize)
    tfidf = tfidf_verctorizer.fit_transform(dataset)
    tfidf_feature_names = tfidf_verctorizer.get_feature_names()

    #lda
    print 'lda...'
    for i in xrange(1,25):
        lda = LatentDirichletAllocation(n_topics = i,learning_method='batch',max_iter=10, \
        random_state=1, n_jobs= 2)
        lda.fit(tfidf)
        #score = lda.score(tfidf)
        #perp = lda.perplexity(tfidf)
        #print i,' ',score,' ',perp
        content = print_top_words(lda, tfidf_feature_names, 10)
        
        f = open('/home/ding/Desktop/LDAModel/topic--{}'.format(i),'w')
        f.write(content)
        f.close()

    #draw pic
    #import matplotlib.pyplot as plt
    #plt.figure()
    #ax = plt.subplot(111)
    #ax.scatter(id[:],pers[:])
    #plt.show()
    #test
    #testset = 'can you a apple for me'
    #tests = str2word2id(tfidf_feature_names,testset)
    #print predict(lda,tests,tfidf_feature_names)