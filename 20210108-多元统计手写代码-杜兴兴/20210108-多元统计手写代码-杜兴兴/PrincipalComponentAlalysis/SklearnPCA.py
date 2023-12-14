# _*_ encoding:utf-8 _*_
"""
    @ProjectName   :ML_HandWriting
    @DocumentName  :SklearnPCA.py
    @VersionNumber :Python 3.7
    @Author        :Xingxing.Du
    @DataTime      :2020/12/3 : 14:06
    @Tools         :PyCharm
    @Description   :None

"""
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"../load_breast_cancer.csv")

print(df.shape)
pca = PCA(n_components=1)
pca.fit(df)
lowD = pca.transform(df)
print(lowD.shape)
reconD = pca.inverse_transform(lowD)
print(reconD.shape)