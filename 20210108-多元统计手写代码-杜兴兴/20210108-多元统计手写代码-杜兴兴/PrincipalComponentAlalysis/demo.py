# _*_ encoding:utf-8 _*_
"""
    @ProjectName   :ML_HandWriting
    @DocumentName  :demo.py
    @VersionNumber :Python 3.7
    @Author        :Xingxing.Du
    @DataTime      :2020/12/3 : 13:08
    @Tools         :PyCharm
    @Description   :None

"""
import numpy as np

a = [1,2,3,4,5,6,7]
ad = np.array(a)
print(a)
print(np.argsort(a)[:-4:-1])