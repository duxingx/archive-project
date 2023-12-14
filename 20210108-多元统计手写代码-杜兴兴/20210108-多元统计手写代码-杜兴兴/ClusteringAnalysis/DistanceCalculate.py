# _*_ encoding:utf-8 _*_
"""
    @ProjectName   :ML_HandWriting
    @DocumentName  :DistanceCalculate.py
    @VersionNumber :Python 3.7
    @Author        :Xingxing.Du
    @DataTime      :2020/11/26 : 10:58
    @Tools         :PyCharm
    @Description   :None

"""
import numpy as np
import pandas as pd
from sklearn import datasets

X, y = datasets.load_wine(return_X_y=True)
data = np.hstack((X, np.vstack(y)))
print("数据维度：{}".format(data.shape))
df = pd.DataFrame(data)

nd = np.array(df)


def eucli_dist(data1, data2):
    eucli_res = np.sqrt(np.dot(data1 - data2, data1 - data2))
    print("Euclidean distance:{}".format(round(eucli_res, 4)))
    return eucli_res


eucli_dist(nd[1], nd[2])

def manhattan_dist(data1, data2):
    manhattan_res = np.sum(np.abs(data1 - data2))
    print("Manhattan distance:{}".format(round(manhattan_res, 4)))
    return manhattan_res


manhattan_dist(nd[1], nd[2])

def chebyshev_dist(data1, data2):
    chebyshev_res = np.max(np.abs(data1 - data2))
    print("Chebyshev distance:{}".format(round(chebyshev_res, 4)))
    return chebyshev_res


chebyshev_dist(nd[1], nd[2])


def minkowski_dist(data1, data2, p):
    minkowshi_res = np.power(np.sum(np.power(np.abs(data1 - data2), p)), 1/p)
    print("Minkowski distance<p={}>:{}".format(p, round(minkowshi_res, 4)))
    return minkowshi_res


minkowski_dist(nd[1], nd[2], 1)
minkowski_dist(nd[1], nd[2], 2)


# def mahalanobis_dist(data1, data2):
#     X = np.vstack([data1, data2])
#     nddata_cov = np.cov(X, rowvar=False)
#     print(nddata_cov.shape)
#     nddata_inv = np.linalg.inv(nddata_cov)
#     tp = data1 - data2
#     mahalanobis_res = np.sqrt(np.dot(np.dot(tp, nddata_inv), tp.T))
#     print("Mahalanobis distance:{}".format(round(mahalanobis_res, 4)))
#     return mahalanobis_res
#
#
# mahalanobis_dist(nd[1], nd[2])
#


















