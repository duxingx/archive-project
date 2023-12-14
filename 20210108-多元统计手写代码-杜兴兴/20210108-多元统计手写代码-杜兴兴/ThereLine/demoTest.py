# _*_ encoding:utf-8 _*_
"""
    @ProjectName   :
    @DocumentName  :demoTest.py
    @VersionNumber :Python 3.7
    @Author        :Xingxing.Du
    @DataTime      :2020/12/23 : 12:58
    @Tools         :PyCharm
    @Description   :

"""
import numpy as np
import pandas as pd
data0 = np.array([[69,85,117,128,164,202,208,388,446,650,1486,47],
              [1313300,2455000,2300000,2913509,5236800,5683609,5798235,4500000,21000000,5663174,11467300,24508000]])





k = 0
for i in np.arange(len(data[0])):
    if np.mod(i, len(data[0]/3)) == 0:
        k = i
        continue
    else:
        demianX0 = np.median(data[0][k:i])
        print(demianX0)












