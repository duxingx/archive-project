# _*_ encoding:utf-8 _*_
"""
    @ProjectName   :ML_HandWriting
    @DocumentName  :MaxVarPCA.py
    @VersionNumber :Python 3.7
    @Author        :Xingxing.Du
    @DataTime      :2020/12/3 : 11:17
    @Tools         :PyCharm
    @Description   :None

"""

import numpy as np
import pandas as pd


if __name__ == '__main__':
    path = r"../load_breast_cancer.csv"
    # names = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14']
    df = pd.read_csv(path)
    dataMat0 = np.array(df.iloc[:, :-1])
    dataMat = dataMat0 - np.mean(dataMat0, axis=0)    # 数据减去均值

    covDataMat = np.cov(dataMat, rowvar=0)
    eigVals, eigVects = np.linalg.eig(covDataMat)

    sumVars = np.sum(eigVals)
    percentage = 0.9
    tempSumVars = 0
    k = 0
    for eigVal in np.sort(eigVals)[::-1]:
        print(eigVal)
        k += 1
        tempSumVars += eigVal
        if tempSumVars / sumVars >= percentage:
            print(k)
            break

    kDimPos = np.argsort(eigVals)[::-1][:k]
    redEigVects = eigVects[:, kDimPos]  # 主成分方向
    print(redEigVects.shape)
    lowDimDataMat = np.dot(dataMat, redEigVects)
    print(lowDimDataMat)




    # max_var_pca(dataMat, percentage=0.9)