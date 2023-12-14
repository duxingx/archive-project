# _*_ encoding:utf-8 _*_
"""
    @ProjectName   :ML_HandWriting
    @DocumentName  :Demo2.py
    @VersionNumber :Python 3.7
    @Author        :Xingxing.Du
    @DataTime      :2020/11/28 : 8:57
    @Tools         :PyCharm
    @Description   :None

"""
import numpy as np
import pandas as pd
# a = np.array([1,2,3,4,5])
# b = np.array([6,3,4,7,8])
# c = np.array([1,2,3,4,5])
#
# a = np.array([(2.5, 2.3), (1.5, 1.3), (2.2, 2.9), (2.1, 2.7), (1.7, 1.9)])
# print(a)
# print(np.cov(a, rowvar=False))
# D = pd.DataFrame()
# x = np.cov(a,b)
# print(x)

# aT = a.T
# print(a)
# print(aT)
#
# D = np.cov(aT)
#
# invD = np.linalg.inv(D)
# print(invD)
#
# tp = a[0] -a[1]
# print(tp)
# print(np.sqrt(np.dot(np.dot(tp,invD),tp.T)))
#
# x = np.random.random(10)
# y = np.random.random(10)
# # 此处进行转置，表示10个样本，每个样本2维
# X = np.vstack([x, y])
# XT = X.T
#
# # 方法一：根据公式求解
# S = np.cov(X)  # 两个维度之间协方差矩阵
# SI = np.linalg.inv(S)  # 协方差矩阵的逆矩阵
# # 马氏距离计算两个样本之间的距离，此处共有10个样本，两两组合，共有45个距离。
# n = XT.shape[0]
# d1 = []
# for i in range(0, n):
#     for j in range(i + 1, n):
#         delta = XT[i] - XT[j]
#         d = np.sqrt(np.dot(np.dot(delta, SI), delta.T))
#         d1.append(d)
# print('d1:', d1)


print(np.zeros((4,3)))

x = np.random.randint(147, size=147)
print(x)














