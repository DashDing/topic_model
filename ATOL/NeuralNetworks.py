#encoding:utf-8
#ding
#2017 07 11

from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.utilities import percentError
from model.classes import doc
from model.funcs import *
from model.config import *


from pybrain.structure import TanhLayer
from pybrain.structure import SigmoidLayer

def buildNet(input_nodes,output_nodes):
    #new a network
    from pybrain.tools.shortcuts import FeedForwardNetwork
    net = FeedForwardNetwork()

    #layers
    hiddenLayerNodes = [10000,5000,400]
    from pybrain.structure import LinearLayer
    inLayer = LinearLayer(input_nodes, name= 'inLayer')
    outLayer = LinearLayer(output_nodes, name= 'outLayer')
    hiddenLayers = []
    for i in xrange(len(hiddenLayerNodes)):
        hiddenLayers.append(SigmoidLayer(hiddenLayerNodes[i], name= 'hiddenLayer{}'.format(i)))
    net.addInputModule(inLayer)
    net.addOutputModule(outLayer)
    for i in xrange(len(hiddenLayerNodes)):
        net.addModule(hiddenLayers[i])

    #net
    from pybrain.structure import FullConnection
    if len(hiddenLayerNodes) >0:
        in_to_hidden = FullConnection(inLayer,hiddenLayers[0])
        hidden_to_out = FullConnection(hiddenLayers[-1],outLayer)
        hidden_to_hidden = []
        for i in xrange(len(hiddenLayers)-1):
            hidden_to_hidden.append(FullConnection(hiddenLayers[i],hiddenLayers[i+1]))
        net.addConnection(in_to_hidden)
        net.addConnection(hidden_to_out)
        for i in xrange(len(hiddenLayers)-1):
            net.addConnection(hidden_to_hidden[i])
    else:
        in_to_out = FullConnection(inLayer,outLayer)
        net.addConnection(in_to_out)

    net.sortModules()
    return net




def NeuralNetworks(data_set,label_set):

    # networks
    net = buildNet(len(data_set[0]),len(label_set[0]))
    #net = buildNetwork(len(data_set[0]),len(label_set[0]),bias = True, hiddenclass = SigmoidLayer)
    # data set
    ds = SupervisedDataSet(len(data_set[0]),len(label_set[0]))
    for i in xrange(len(label_set)):
        ds.addSample(data_set[i],label_set[i])
    # train
    trainer = BackpropTrainer(net, ds, momentum= 0.0,verbose= True,weightdecay= 0.0)
    #trainer.train()
    trainer.trainUntilConvergence(maxEpochs = 200)
    #for i in xrange(200):
    #    trainer.trainEpochs(10)
    #trainresult = percentError(trainer.testOnClassData(),ds['target'])
    #print "epoch: %4d" % trainer.totalepochs, "train error %5.2f%%" % trainresult
    #for input, target, in ds:
    #    print input,target,net.activate(input)
    return net

def classifier(TopKeywords=0, c_train_label=dict(), c_test_label=dict()):

    # train
    # read train data
    print 'read c_train data from file ...'
    c_train_files = readFiles(c_train_path, c_train_label)
    # k_expert dict->list
    print 'l_train sort and k_expert list ...'
    l_train_sorted, k_expert_list = dict2list(k_expert, l_train)
    # word to id
    print 'c_train init, make dic ...'
    dic, c_train_id, c_train_label, c_train_m, k_expert_id = word2ID( \
        k_expert_list, c_train_files, l_train_sorted, lamda)
    len_dic = len(dic)

    # tf-icf
    print 'train data -> tf-icf ...'
    d_train = []
    d_train_l = []
    for docu in xrange(len(c_train_m)):
        L = []
        for i in xrange(len(l_train_sorted)):
            if i in c_train_label[docu]:
                L.append(1)
            else:
                L.append(0)
        d_train_l.append(L)

    print 'init classifiers ...'
    import  time
    print time.localtime()
    net = NeuralNetworks(c_train_id, d_train_l)
    import  time
    print time.localtime()
    return
    # test
    print 'choice test file ...'
    c_test_files = readFiles(c_test_path, c_test_label)
    c_test_files_id = [doc2id(doc, dic, l_train_sorted) for doc in c_test_files]

    # score
    print 'testing ...'
    count = 0.
    right = .0

    # predict_proba test

    for c_test_index in xrange(len(c_test_files_id)):
        count += 1
        content = c_test_files_id[c_test_index].getContent()
        labels = c_test_files_id[c_test_index].getLabels()
        predict_result = net.activate(content)
        for i in xrange(len(predict_result)):
            if predict_result[i] >= 0.5 and i in labels:
                right +=1
                break

    print 'test finished: score {}'.format(right / count)
    return right / count

if __name__ == '__main__':
    test = 0
    if test == 0:

        # shi ze jiao cha
        c_train_label = dict(c_train_label_default)
        l_train.sort()
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
            a = classifier(10, c_train_label=c_t, c_test_label=c_test)
            nb.append(a)
            break
        print 'NB:{}\n'.format(nb)

    else:
        data_set = [[0,0],[0,1],[1,0],[1,1]]
        label_set = [[0,1],[0,0],[1,1],[1,0]]
        for i in xrange(0):
            for j in xrange(4):
                data_set.append(data_set[j])
                label_set.append(label_set[j])
        net = NeuralNetworks(data_set,label_set)
        #net.
        print net.activate([1,0])