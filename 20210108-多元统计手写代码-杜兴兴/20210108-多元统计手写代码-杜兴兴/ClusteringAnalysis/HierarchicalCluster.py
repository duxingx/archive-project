# _*_ encoding:utf-8 _*_
"""
    @ProjectName   :ML_HandWriting
    @DocumentName  :HierarchicalCluster.py
    @VersionNumber :Python 3.7
    @Author        :Xingxing.Du
    @DataTime      :2020/11/28 : 10:43
    @Tools         :PyCharm
    @Description   :this module is used to ....

"""
from ClusteringAnalysis.demo import write_to_file
import pandas as pd
import numpy as np

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


def shouldStop(oldCentroids, centroids, iterations, maxIt):
    """
    func:可迭代条件判定
    :param oldCentroids: 原来的质心
    :param centroids: 现在的质心
    :param iterations: 已迭代的次数
    :param maxIt: 可迭代的最大次数
    :return: True or False
    """
    if iterations > maxIt: # 达到最大迭代次数要求
        return True
    else:
        return np.array_equal(oldCentroids, centroids)  # 还可继续迭代,但质心不在变化


def getLabel(dataSetRow, class_centroids):
    """
    func:获取聚类标签
    :param dataSetRow:
    :param class_centroids:
    :return:
    """
    label = class_centroids[0, -1]  # 初始化分类标签,随机指定第一个质心
    minDist = np.linalg.norm(dataSetRow - class_centroids[0, :-1])  # 样本与第一个质心的距离,初始化最小距离
    for i in range(1, class_centroids.shape[0]):  # 计算样本与所有质心的距离
        dist = np.linalg.norm((dataSetRow - class_centroids[i, :-1]))
        if dist < minDist:
            minDist = dist
            label = class_centroids[i, -1]
    # print("minDist:{}".format(minDist))
    # print("label:{}".format(label))
    return label
def updateLabels(dataSet, class_centroids):
    numPoints, numDim = dataSet.shape
    for i in range(numPoints):
        dataSet[i, -1] = getLabel(dataSet[i, -1], class_centroids)  # 更新样本的聚类标签结果
    pass
def getCentroids(dataSet, k):
    result = np.zeros(k, dataSet.shape[1])
    for i in range(1, k+1):
        oneCluster = dataSet[dataSet[:, -1] == i, :-1]  # 所有已被聚类为i类的样本
        result[i - 1, :-1] = np.mean(oneCluster, axis=0)
        result[i - 1, -1] = i
    return result

    # 距离最近的两个样本聚为一类,直到所有样本聚为一类;
        # 计算所有样本之间的距离矩阵:欧式距离/M氏距离/绝对值距离.../相似度
        # 选择最小距离的两个样本,合并为一类
        # 计算新的这个类和其他样本的距离:最短距离法/最长距离法/平均距离法/质心连接法/
        # 选择最小距离的两个样本,合并为一类
        # 以此类推,直到所有样本为一类,结束;
def hierar_cluster(inputdata, k, dist_method, cluster_method, cluster_class_num, maxIt):
    # 需要聚类的数据集
    dataSet = np.zeros((inputdata.shape[0], inputdata.shape[1] + 1))
    dataSet[:, :-1] = inputdata

    # 开始所有n个样本划分为k类,k提前指定;  class_centroids[k,numDim+1]
    rand_k = np.random.randint(inputdata.shape[0], size=k)
    class_centroids = dataSet[rand_k, :]
    class_centroids[:, -1] = range(1, k + 1)

    oldCentroids = None
    iterations = 0

    for i in range(len(dataSet)):  # 计算每个样本与所有已经聚类的类的距离,将样本聚类为最小距离的类
        dataSet[i, -1] = class_centroids[0, -1]
        minSampleWithClassDist = np.linalg.norm(dataSet[i, :-1],class_centroids[0, :-1])
        for j in range(1, len(class_centroids)):
            sampleWithClassDist = np.linalg.norm(dataSet[i, :-1],class_centroids[j, :-1])
            if sampleWithClassDist < minSampleWithClassDist:
                minSampleWithClassDist = sampleWithClassDist
                # 将样本的标签指定为最小距离的那类
                label = class_centroids[j, -1]
                dataSet[i, -1] = label



    # while not shouldStop(oldCentroids, class_centroids, iterations, maxIt):
    #     print("iteration:{}".format(iterations))
    #     print("dataSet:{}".format(dataSet))
    #     print("centroids:{}".format(class_centroids))
    #
    #     oldCentroids = np.copy(class_centroids)
    #     iterations += 1
    #
    #     updateLabels(dataSet, class_centroids)
    #
    #     class_centroids = getCentroids(dataSet, k)

    return dataSet


if __name__ == '__main__':
    path = r"C:\Users\14983\Desktop\load_wine.csv"
    data = file_to_read(file_path=path, header=0)
    # print(type(data))
    nyd = data_preprocess(data)
    print(nyd)
    print(nyd.shape)
    # result = hierar_cluster(data)
    # write_to_file(path, result)






