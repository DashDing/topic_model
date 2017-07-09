import numpy as np

if __name__ == '__main__':
    #init
    nlist = [0.6224489795918368, 0.6494845360824743, 0.5151515151515151, 0.6060606060606061, 0.5612244897959183, 0.6262626262626263, 0.5918367346938775, 0.5339805825242718, 0.5849056603773585, 0.5471698113207547]
    narray = np.array(nlist)
    sum = narray.sum()
    mean = sum/len(nlist)
    narray2=narray*narray
    sum2 = narray2.sum()
    var = sum2/len(nlist)-mean**2
    print mean
    print var