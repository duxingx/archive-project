# coding=utf-8
import pandas as pd
import csv

# 显示所有列
#pd.set_option('display.max_columns', None)
# 显示所有行
#pd.set_option('display.max_rows', None)

df = pd.read_csv('月度数据-合.csv', encoding='utf-8-sig')
#df=df.fillna('空值')
#print(df.describe)
c_columns=df.columns[:63]
c_df=df[c_columns]
print(c_df.describe)
c_df.dropna(axis=0,thresh=2,inplace=True)#删除那些少于2个非空值的行
c_df=pd.melt(c_df, id_vars=["指标"],
              value_vars=c_columns[1:],
              var_name="年月",
              value_name="指标值")
print(c_df)






