import numpy as np

if __name__ == '__main__':
    #init
    nlist = [0.7346938775510204, 0.7628865979381443, 0.696969696969697, 0.7070707070707071, 0.6938775510204082, 0.6868686868686869, 0.7244897959183674, 0.6699029126213593, 0.7358490566037735, 0.6698113207547169]


    narray = np.array(nlist)
    sum = narray.sum()
    mean = sum/len(nlist)
    narray2=narray*narray
    sum2 = narray2.sum()
    var = sum2/len(nlist)-mean**2
    print mean
    print var