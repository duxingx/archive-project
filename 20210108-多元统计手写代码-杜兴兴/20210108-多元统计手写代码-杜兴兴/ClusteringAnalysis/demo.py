# _*_ encoding:utf-8 _*_
"""
    @ProjectName   :ML_HandWriting
    @DocumentName  :demo.py
    @VersionNumber :Python 3.7
    @Author        :Xingxing.Du
    @DataTime      :2020/11/26 : 11:20
    @Tools         :PyCharm
    @Description   :None

"""
import numpy as np
import os

vector1 = np.array([1, 2, 3])
vector2 = np.array([4, 5, 6])
# print(vector1 - vector2)
# print(np.sqrt(np.dot(vector1 - vector2,vector1 - vector2)))

# op1 = np.sqrt(np.sum(np.square(vector1 - vector2)))
# op2 = np.linalg.norm(vector1 - vector2)
# print(op1)
# print(op2)

#
# x = os.path.exists(r"D:\DuXingxing\04_interest\01_blog\01_Markdown\统计相关.md")
# print(x)
#
# y = os.listdir(r"D:\DuXingxing\04_interest\01_blog\01_Markdown\01_MachineLearning")
# print(y)
#
# a = list()
# for i in y:
#     print(i.split(".")[0])
#
# os.makedirs(r"D:\test.txt", exist_ok=True)


def write_to_file(path, file_name="untitled.txt", content=""):
    """
    func: 此类用于将内容写出到指定路径，并生成文件
    :param path: 路径
    :param file_name:文件名
    :param content: 需要写出的内容
    :return: None
    """
    if os.path.exists(path=path):
        path_file = os.path.join(path, file_name)
        with open(path_file, mode='w', encoding='utf-8') as fp:
            fp.write(content)
            print("The file was written successfully : <{}>".format(path_file))


# write_to_file(path="D:/Temp", file_name="test.txt", content="adsfasfasfd")


