# _*_ encoding:utf-8 _*_
"""
    @ProjectName   :ML_HandWriting
    @DocumentName  :BayesDiscrimination.py
    @VersionNumber :Python 3.*
    @Author        :14983
    @DataTime      :14:06
    @Tools         :PyCharm
    @Description   :None

"""

import pandas as pd
import numpy as np
import logging
import math

from sklearn.model_selection import train_test_split

logging.basicConfig(format='%(filename)s[line:%(lineno)d]-%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)

class Bayes_classfier:
    """
    class: 贝叶斯分类器
    功能：
        - 读取加载数据集
        - 数据划分
        - 模型训练
        - 模型预测
        - 模型参数保存
    """

    def __init__(self, path):
        # 模型数据集路径
        self.data_path = path
        # 模型参数记录
        self.params = dict()

    def data_processing(self):
        """
        func: 数据集读取与训练测试集划分
        return:None
        """
        self.df = pd.read_csv(self.data_path, header=None)
        logging.info('loading datasets,volume:{}'.format(self.df.shape))
        # 数列名指定
        self.df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']

        # 特征与标签提前
        features = self.df
        label = self.df['species']
        # 训练集与测试集切分
        self.X_train, self.X_valid, self.y_train, self.y_valid = train_test_split(features, label, test_size=0.25,
                                                                                  random_state=300, stratify=label)

        logging.info('split datasets, train_datasets:{},test_datasets:{}'.format(self.X_train.shape, self.X_valid.shape))

        pass

    def fit(self):
        """
        func: 模型训练过程，即计算贝叶斯各个参数

        return: None
        """
        # 计算先验概率
        priori_prob = (self.y_train.value_counts()+1)/(self.y_train.shape[0]+3)
        logging.info('计算训练集先验概率....')
        # 记录各模型参数的值用于预测
        self.params['priori_prob'] = priori_prob

        # 计算各类均值mu，协方差矩阵的逆，协方差阵的行列式
        mu_ = dict()
        sigma_inv = dict()
        det_ = dict()
        logging.info('计算mu,sigma等矩阵运算...')
        for _label, groups in self.X_train.groupby(['species']):
            groups = groups[[x for x in self.df.columns if x not in ['species']]]

            mu_[_label] = groups.mean(axis=0)
            sigma_ = np.cov(groups.T, bias=True)
            sigma_inv[_label] = np.linalg.inv(sigma_)
            det_[_label] = np.linalg.det(sigma_)
        self.params['class_mu'] = mu_
        # print(self.params['class_mu'])
        self.params['class_sigma_inv'] = sigma_inv
        # print(self.params['class_sigma_inv'])
        self.params['class_det'] = det_
        # print(self.params['class_det'])

    def g(self, x, mu, sigma_inv, det, priori_prob):
        """
        func: 分类判别函数，即利用代码实现判别函数
        return: 判别值
        注：@ 为numpy矩阵乘法运算
        """
        return -0.5*(x - mu).T @ sigma_inv @ (x - mu) - 0.5 * math.log(det) + math.log(priori_prob)   # 广义平方距离

    def predict(self):
        # 对各类进行测试
        for _label, test_group in self.X_valid.groupby(['species']):
            logging.info('test the {},volume:{}'.format(_label, test_group.shape[0]))
            test_feature = test_group[[x for x in self.df.columns if x not in ['species']]]
            #
            print(_label)
            # 记录测试结果是否正确
            test_res = []

            for _, row in test_feature.iterrows():
                score = dict()

                # 计算各类别的得分情况
                for _l in self.df['species'].unique():
                    score[_l] = self.g(np.array(row.values),
                                       self.params['class_mu'][_l].values,  # 以下参数均是从训练集计算而得
                                       self.params['class_sigma_inv'][_l],
                                       self.params['class_det'][_l],
                                       self.params['priori_prob'][_l])
                predict_res = max(score, key=score.get)   # 最大后验概率  最小广义平方距离

                print('[测试当前预测类别：{}，实际类别：{}，{}'.format(predict_res, _label, predict_res == _label))
                test_res.append(predict_res == _label)
            print('{}类别测试准确率：{}'.format(_label, test_res.count(True)/len(test_res)))


classfier = Bayes_classfier('C:/Users/14983/Desktop/iris.csv')
classfier.data_processing()
classfier.fit()
classfier.predict()