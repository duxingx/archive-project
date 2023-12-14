# _*_ encoding:utf-8 _*_
"""
    @ProjectName   :ML_HandWriting
    @DocumentName  :demo.py
    @VersionNumber :Python 3.*
    @Author        :14983
    @DataTime      :18:28
    @Tools         :PyCharm
    @Description   :None

"""
import numpy as np
import pandas as pd
from sklearn import datasets

X, y = datasets.load_breast_cancer(return_X_y=True)
y = np.vstack(y)
print(X.shape)
print(y.shape)
data = np.hstack((X, y))
print(data.shape)
data = pd.DataFrame(data)
# data.groupby()
data.to_csv(r'../load_breast_cancer.csv', header=None, index=None)
#
# columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
# print(columns[-1], type(columns[-1]))