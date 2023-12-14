# _*_ encoding:utf-8 _*_
"""
    @ProjectName   :ML_HandWriting
    @DocumentName  :FisherDiscrimination.py
    @VersionNumber :Python 3.7
    @Author        :Xingxing.Du
    @DataTime      :2020/11/25 14:08
    @Tools         :PyCharm
    @Description   :None

"""

import numpy as np
import pandas as pd


class fisher_discrimination:
    """
    func:
        -对样本进行fisher判别
        -计算类内均值，类内协方差
        -计算方向向量
        -对样本的类别进行判别
    """

    def __init__(self, datasets):
        # 模型数据:训练集,dataframe
        self.train = datasets
        # 模型参数记录
        self.params = dict()

    def cal_cov_and_avg(self, var_class):
        """
        func:
            -本方法用于计算类别的协方差阵和均值向量(训练样本)
        params:
            -var_class:分类变量
        return:
            -mu:协方差阵
            -cov:均值向量
        """
        mu = dict()
        cov = dict()
        for label, groups in self.train.groupby([var_class]):
            groups = groups[[x for x in groups.columns if x not in [var_class]]]  # 不计算分类变量
            mu[label] = groups.mean(axis=0)  # 均值向量
            cov[label] = np.zeros((groups.shape[1], groups.shape[1]))  # 初始化协方差阵
            # 此循环用于计算协方差阵
            for i in range(len(groups)):
                sample0 = groups.iloc[i] - mu[label]
                sample = np.array(sample0.tolist())
                cov[label] += sample * sample.reshape(sample.shape[0], 1)
        return mu, cov

    def fisher_rule(self, var_class):
        """
        func：
            -本方法用于确定方向向量w
        params:
            -var_class:分类变量
        return：
            -w:投影的方向向量
        """
        mu_i = dict()
        cov_i = dict()
        mu_all = self.train.mean(axis=0)
        s_w = np.zeros((self.train.shape[1] - 1, self.train.shape[1] - 1))
        s_b = np.zeros((self.train.shape[1] - 1, self.train.shape[1] - 1))
        mu_i, cov_i = self.cal_cov_and_avg(var_class)
        # 此循环用于计算总的类内散度矩阵,类间散度矩阵
        for label, groups in self.train.groupby([var_class]):
            groups = groups[[x for x in groups.columns if x not in [var_class]]]

            s_w += cov_i[label]  # 类内散度矩阵
            print("{}的类内散度矩阵:".format(label))
            print(cov_i[label])
            class_mu0 = mu_i[label] - mu_all
            class_mu = np.array(class_mu0.tolist())
            s_b_i = (class_mu * class_mu.reshape(class_mu.shape[0], 1)) * len(groups)
            s_b += s_b_i  # 类间散度矩阵
            print("{}的类间散度矩阵：".format(label))
            print(s_b_i)
            print("===========================================================")
        print("总的类内散度矩阵:")
        print(s_w)
        print("总的类间散度矩阵:")
        print(s_b)
        print("===========================================================")
        u, s, v = np.linalg.svd(s_w)  # 奇异值分解（s_w可能存在不可逆的情况）
        s_w_inv = np.dot(np.dot(v.T, np.linalg.inv(np.diag(s))), u.T)  # 广义逆
        w_a = np.dot(s_w_inv, s_b)
        w_val, w_vec = np.linalg.eig(w_a)  # 计算所有特征值和特征向量
        w = w_vec[:, np.argmax(w_val)]  # 选择最大特征值的特征向量

        return w

    def judge(self, sample, w, var_class):
        """
        func:
            本方法用于对样本进行判别
        return:
            -min_key:判别结果
        """
        res = dict()
        pos = np.dot(w.T, sample)
        # pos = # 样本点的投影
        mu_i, cov_i = self.cal_cov_and_avg(var_class)

        for label, groups in self.train.groupby([var_class]):
            center_i = np.dot(w.T, mu_i[label])  # 类内均值向量在方向向量上的投影

            # res[label] = np.dot(pos - center_i, pos - center_i)
            res[label] = abs(pos - center_i)

        min_key = min(res, key=res.get)
        # print(min_key)
        return min_key


def method_name(t):
    """
    全局方法
    :param t: 传入的数据，DataFrame格式
    :return: None
    """
    # 判别测试样本
    test_res = list()
    test_label = list()
    count = 0
    corrected = list()
    for i in range(len(t)):
        test_res.append(fisher_sub.judge(t.loc[i, t.columns[:-1]], w, t.columns[-1]))
        test_label.append(t.loc[i, t.columns[-1]])
        # 评估判别结果
        if test_res[i] == test_label[i]:
            count += 1
            corrected.append(True)
        else:
            corrected.append(False)
    T_rate = count / len(corrected)
    print("全样本回判的综合正确率：", T_rate * 100, "%")


def import_data(path):
    """
    全局类方法
    :param path: 数据路径，csv，xls等格式,注意最后一列为分类变量，且str格式;
    :return: DataFrame
    """
    # 导入数据
    path = path
    df = pd.read_csv(path, header=0)
    # df.columns = val_name
    return df


# 调用函数实现
# 测试iris数据
if __name__ == '__main__':
    # 导入数据
    df = import_data(path=r'C:/Users/14983/Desktop/load_wine.csv')

    # 根据训练样本计算投影方向向量
    fisher_sub = fisher_discrimination(df)
    w = fisher_sub.fisher_rule(df.columns[-1])
    print("最佳投影的方向向量：", w)

    # 回判检验效果
    method_name(df)
