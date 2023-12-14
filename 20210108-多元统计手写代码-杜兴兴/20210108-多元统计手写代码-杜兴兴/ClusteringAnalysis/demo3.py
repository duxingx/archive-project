# _*_ encoding:utf-8 _*_
"""
    @ProjectName   :ML_HandWriting
    @DocumentName  :demo3.py
    @VersionNumber :Python 3.7
    @Author        :Xingxing.Du
    @DataTime      :2020/11/28 : 19:17
    @Tools         :PyCharm
    @Description   :None

"""



import pandas as pd
import numpy as np
from sklearn import cluster
cluster


def file_to_read(file_path, header=None, names=None):
    """
    func:导入数据,数据格式支持csv,xls,xlsx
    :param file_path: 文件路径
    :param header: 指定变量名索引,默认为0
    :param names: 指定变量名
    :return: DataFrame格式的data
    """
    if file_path.split('.')[1] == 'csv':
        df_data = pd.read_csv(file_path, header=header, names=names)
        print("'csv'格式的数据文件导入成功!")
    elif file_path.split('.')[1] in ['xls', 'xlsx']:
        df_data = pd.read_excel(file_path, header=header, names=names)
        print("'xls'格式的数据文件导入成功!")
    else:
        df_data = None
        print("请传入'csv','xls','xlsx'格式的数据文件!")
    return df_data


def data_preprocess(ndy_data):
    """
    func: 数据格式处理
    :param ndy_data: DataFrame
    :return: array
    """
    ny = ndy_data.values
    return ny


def search_min():
    rownum = None
    colnum = None

    min_val = D[1, 0]
    for i in range(len(D)):
        for j in range(len(D)):
            if i <= j:
                continue
            if D[i, j] <= min_val:
                min_val = D[i, j]
                rownum = i
                colnum = j

    return rownum, colnum, min_val


if __name__ == '__main__':
    path = r"C:\Users\14983\Desktop\load_wine.csv"
    data = file_to_read(file_path=path, header=0)
    # print(type(data))
    nyd = data_preprocess(data)
    print(nyd)
    print(nyd.shape)

    print("====================================================")
    # print("x_mean:", x_mean,x_mean.shape)
    # print(nyd[:,-1], type(nyd[:, -1]))
    # print(np.unique(nyd[:, -1]))
    n, m = nyd.shape
    D = np.zeros([n, n])

    for i in range(n):
        for j in range(i+1, n):
            D[i, j] = np.round(np.linalg.norm(nyd[i, :-1] - nyd[j, :-1]), decimals=2)
            D[j, i] = D[i, j]
    # print(D)
    print(D.shape)

    rownum, colnum, min_val = search_min()

    # new_ar = np.zeros([1,n])
    # for i in range(len(D)):
    #     new_ar[:, i] =np.mean(np.row_stack((D[rownum,:],D[colnum, :])),axis=1)
    #
    # print(new_ar,"this is zeros")

    xxx = np.max(np.row_stack((D[rownum,:],D[colnum, :])),axis=0)
    res = np.row_stack((D, xxx))
    print("res.shape:",res.shape)
    print("xxx.reshape:",xxx.reshape(-1,1).shape)
    res2 = np.column_stack((res, xxx.reshape(-1,1)))
    print(res2.shape)
    del_D = np.delete(res,(rownum,colnum),axis=0)
    del_D_col = np.delete(del_D,(rownum,colnum),axis=1)

    print("======================================================")
    print(del_D_col)
    print(del_D_col.shape)
    print("======================================================")
    # print(xxx,xxx.shape)

    # print("search:============",search_min())
    #
    # x_mean_cls = dict()
    # for cls in np.unique(nyd[:, -1]):
    #     x_mean = np.mean(nyd[nyd[:, -1] == cls, :-1], axis=0)
    #     x_mean_cls[cls] = x_mean
    # # print(x_mean_cls)
    #
    # # res = np.array(list())
    # list_m = list(x_mean_cls.values())
    # # print(list_m)
    #
    # print("====================================================")
    # for i in range(len(nyd)):
    #     dist = dict()
    #     for key, value in x_mean_cls.items():
    #         if nyd[i, -1] == key:
    #             continue
    #         dist[key] = np.linalg.norm(value - nyd[i, :-1], ord=2)
    #     nyd[i, -1] = min(dist,key=dist.get)
    # print(nyd)
