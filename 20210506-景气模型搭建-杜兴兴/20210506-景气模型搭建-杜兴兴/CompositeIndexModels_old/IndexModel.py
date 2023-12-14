# _*_ encoding:utf-8 _*_

import re
import pandas as pd
import numpy as np
import mysql.connector
from cif import cif
from dateutil.relativedelta import relativedelta
from chinese_calendar import is_workday
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings("ignore")


def date_parse(date_str):
    """
    将字符串的日期格式处理为datetime
    :param date_str:2001年1月
    :return:pd.datetime
    """
    date_str1 = date_str.str.split('月').str[0].add('月01日')
    date_str2 = date_str1.str.replace('年', '-').str.replace('月', '-').str.replace('日', '')
    date = pd.to_datetime(date_str2, format='%Y-%m-%d', errors='coerce')
    return date


def select_month(df, month):
    """
    根据索引选取指定月份数据
    :param df:DataFrame
    :param month: 指定月份(1/2/3/...)
    :return:子集
    """
    month_select = df.index[pd.Series(df.index).dt.month.isin(month)]
    return month_select


def month_weights(month1, month2):
    """
    计算指定月份的权重
    :param month1: 指定月份(DateTime格式)
    :param month2: 指定月份(DateTime格式)
    :return:month1，month2的权重(DataFrame格式)
    """
    weight1 = pd.DataFrame(index=month1, columns=["workdays"])
    weight2 = pd.DataFrame(index=month2, columns=["workdays"])

    for i, j in zip(month1, month2):
        # 计算month1，month2的工作日天数
        month_workday1 = np.sum(pd.date_range(i, i + relativedelta(months=1))[1:-1].map(is_workday))
        month_workday2 = np.sum(
            pd.date_range(i + relativedelta(months=1), i + relativedelta(months=2))[1:-1].map(is_workday))
        # 根据工作日天数计算权重
        weight1.loc[i, "workdays"] = month_workday1 / (month_workday1 + month_workday2)
        weight2.loc[j, "workdays"] = month_workday2 / (month_workday1 + month_workday2)

    return weight1, weight2


def accumulation_process(Long_df, note_class="当月累计值"):
    """
    对当月累计类别指标的同比转换
    :param Long_df: 需要处理的DataFrame
    :param note_class: 根据note的值筛选
    :return: 同比处理之后的长数据DataFrame
    """

    Pivot_data = Long_df[Long_df["note"] == note_class].pivot(columns="indicators", values="value")

    # 选取一月、二月
    Jan = select_month(Pivot_data, [1])
    Feb = select_month(Pivot_data, [2])
    # Mar = select_month(Pivot_data, [3])
    Jan_Feb = select_month(Pivot_data, [1, 2])

    # 计算一月权重
    weights1, weights2 = month_weights(Jan, Feb)

    # 用二月的数据填补一月
    Pivot_data.loc[Jan_Feb] = Pivot_data.loc[Jan_Feb].fillna(method="bfill")

    # 对1月份数据根据权重计算(2月是累计值，不进行修改)
    Pivot_data.loc[Jan] = Pivot_data.loc[Jan].mul(weights1["workdays"], axis=0)
    # Pivot_data.loc[Feb] = Pivot_data.loc[Feb].mul(weights2["workdays"],axis=0)

    # 计算当月值(1月份不需要一阶差分)
    month_data = Pivot_data.diff(1)
    month_data.update(Pivot_data.loc[Pivot_data.index[pd.Series(Pivot_data.index).dt.month == 1]])

    # 计算同比增长
    month_tongbi_data = month_data.pct_change(periods=12).replace([np.inf, -np.inf], 0) * 100
    # month_tongbi_data.dropna(how="all", inplace=True)

    # 转为长数据
    accu_process = pd.melt(month_tongbi_data.reset_index(), id_vars=["time"]).set_index("time")

    return accu_process


def variable_process(df, note_value=None, measure_value=None, split_str1="_", split_str2="("):
    """
    对数据集的变量处理
    :param df: 长数据
    :param note_value: note的值
    :param measure_value: measure的值
    :param split_str2:指标划分“subject”的分隔符1
    :param split_str1:指标划分“measure”的分隔符2
    :return: 变量处理后的DataFrame
    """
    Long_df = df.copy()
    Long_df.loc[:, "note"] = note_value
    # Long_df.loc[:, "note"] = "Statistical Bureau"

    # Long_df.loc[:, "subject"] = \
    #     Long_df.loc[:, "indicators"].str.split(split_str1, expand=True)[1].str.split(split_str2, expand=True)[0]
    Long_df.loc[:, "subject"] =Long_df.loc[:,"indicators"]

    if measure_value:
        Long_df.loc[:, "measure"] = measure_value
    else:
        Long_df.loc[:, "measure"] = Long_df.loc[:, "indicators"].str.findall(r'[(](.*?)[)]', flags=re.S).str.get(-1)

    var_proc = Long_df[["note", "subject", "measure", "value"]]

    return var_proc


def ss_result_process(ss_result=None, name="INDEX_NAME", value="INDEX_VALUE", month="YEAR_MONTH", split_str="$"):
    """
    ss_result数据处理
    :param ss_result:DataFrame数据
    :param name:INDEX_NAME(字符串)
    :param value:INDEX_VALUE(字符串)
    :param month:Date(字符串)
    :param split_str:分隔符号
    :return:
    """
    # 删除重复值、空日期
    ss_result_drop1 = ss_result.drop_duplicates(subset=[name, month], keep='first').copy()
    ss_result_drop = ss_result_drop1.dropna(subset=["YEAR_MONTH"]).copy()

    # 日期设为索引
    ss_result_drop.loc[:, "time"] = pd.to_datetime(ss_result_drop.loc[:, month], format="%Y%m").dt.date
    ss_result_time = ss_result_drop.set_index("time").sort_index()
    ss_result_time.index = pd.DatetimeIndex(ss_result_time.index)

    # 同比转换
    month_data = ss_result_time.pivot(columns='INDEX_NAME', values='INDEX_VALUE').dropna(axis=1, how="all")
    month_tongbi_data = month_data.pct_change(periods=12).replace([np.inf, -np.inf], 0) * 100
    month_tongbi_data_drop = month_tongbi_data.dropna(axis=0, how="all").dropna(axis=1, how="all")
    ss_result_time = pd.melt(month_tongbi_data_drop.reset_index(), id_vars=["time"]).set_index("time").rename(
        columns={"value": "INDEX_VALUE"})

    # 变量处理
    ss_result_time["note"] = ss_result_time[name].str.split(split_str, expand=True)[0].replace([None], "0")
    ss_result_time["note"] = "[SS_Result]"

    # ss_result_time["subject"] = ss_result_time[name].str.split(split_str, expand=True)[1].replace([None], "0")
    ss_result_time["subject"] = ss_result_time[name]
    # ss_result_time["measure"] = ss_result_time[name].str.split(split_str, expand=True)[2].replace([None], "0")
    ss_result_time["measure"] = "%"
    ss_result_time["value"] = ss_result_time[value]

    # 选取变量
    ss_result_proc = ss_result_time[["note", "subject", "measure", "value"]]

    return ss_result_proc


# def ss_result_process(ss_result=None, name="INDEX_NAME", value="INDEX_VALUE", month="YEAR_MONTH", split_str="$"):
#     """
#     ss_result数据处理
#     :param ss_result:DataFrame数据
#     :param name:INDEX_NAME(字符串)
#     :param value:INDEX_VALUE(字符串)
#     :param month:Date(字符串)
#     :param split_str:分隔符号
#     :return:
#     """
#     # 删除重复值
#     ss_result_drop = ss_result.drop_duplicates(subset=[name, month], keep='first').copy()
#     # 日期设为索引
#     ss_result_drop.loc[:, "time"] = pd.to_datetime(ss_result_drop.loc[:, month], format="%Y%m").dt.date
#     ss_result_time = ss_result_drop.set_index("time").sort_index()
#     # 变量处理
#     ss_result_time["note"] = ss_result_time[name].str.split(split_str, expand=True)[0].replace([None], "0")
#     ss_result_time["note"] = "[SS_Result]"
#
#     # ss_result_time["subject"] = ss_result_time[name].str.split(split_str, expand=True)[1].replace([None], "0")
#     ss_result_time["subject"] = ss_result_time[name]
#     # ss_result_time["measure"] = ss_result_time[name].str.split(split_str, expand=True)[2].replace([None], "0")
#     ss_result_time["measure"] = "%"
#     ss_result_time["value"] = ss_result_time[value]
#
#     # 选取变量
#     ss_result_proc = ss_result_time[["note", "subject", "measure", "value"]]
#
#     return ss_result_proc


def data_transform(data_rs_df, data_all_df):
    """

    :param data_rs_df:
    :param data_all_df:
    :return:
    """
    # 参考指标转换

    if data_rs_df.shape[0] > 0:
        rs1 = cif.getRidOfMultiindex(df=data_rs_df)
        rs: pd.DataFrame = cif.getIndexAsDate(rs1)

    # 个体指标转换
    if data_all_df.shape[0] > 0:
        data1 = cif.getRidOfMultiindex(df=data_all_df)
        data: pd.DataFrame = cif.getIndexAsDate(data1)

    # 参考指标：季节调整、离群值过滤、短期预测、周期检测(HP滤波）、归一化
    rs_hp_norm = cif.pipelineTransformations(df=rs, showPlots=False, savePlots=False, createInverse=False)

    # 初筛指标：季节调整、离群值过滤、短期预测、周期检测(HP滤波）、归一化
    data_hp_norm = cif.pipelineTransformations(df=data, showPlots=False, savePlots=False, createInverse=False)

    return data_hp_norm, rs_hp_norm


def turning_point_deal(rs_hp_norm, data_hp_norm):
    """
    根据参考指标，对景气指标进行转折点匹配
    :param rs_hp_norm: 季节处理、标准化后的参考指标
    :param data_hp_norm: 季节处理、标准化后的景气指标
    :return:
        tpd_extOrd:指标序列中匹配的转折点的序号(排序序号)
        tpd_time:匹配的转折点之间的时间差(以月为单位)
        tpd_missing:参考序列中未匹配到的转折点（True or False）
        tpd_missingEarly:在这个时间序列开始之前的时间点 参考序列中出现的转折点（True or False）
        tpd_extra:指标序列中未匹配到的转折点（True or False）
    """

    # 参考指标、景气指标转折点检测（Bry-Boschan算法）
    rs_tp = cif.pipelineTPDetection(df=rs_hp_norm, printDetails=False, showPlots=False, savePlots=False)
    data_tp = cif.pipelineTPDetection(df=data_hp_norm, printDetails=False, showPlots=False, savePlots=False)

    # 匹配转折点
    tpd_extOrd, tpd_time, tpd_missing, tpd_missingEarly, tpd_extra = cif.pipelineTPMatching(df1=rs_hp_norm,
                                                                                            df2=data_hp_norm,
                                                                                            ind1=rs_tp, ind2=data_tp,
                                                                                            printDetails=False,
                                                                                            showPlots=False,
                                                                                            savePlots=False,
                                                                                            lagFrom=-24, lagTo=24)

    return tpd_extOrd, tpd_time, tpd_missing, tpd_missingEarly, tpd_extra, rs_tp, data_tp


def kl_info_compute(data_hp_norm, rs_hp_norm, n=None, tl=12):
    def kl_info(x_index, y_index, sample, lag_num=tl):
        """
        此函数用于计算K-L信息量：基准变量与被选择变量超前或滞后若干期
        :param x_index:时序指标, float
        :param y_index:基准指标, float
        :param sample: 总样本量
        :param lag_num: 最大延迟阶数
        :return: 返回kl信息量和对应的延迟阶数
        """
        if sample is None:
            sample = len(x_index)

        res = []
        time_lag = None

        px = np.array(x_index / np.sum(x_index))
        py = y_index / np.sum(y_index)

        for lag in range(-lag_num, lag_num + 1):

            k = 0

            if lag > 0:
                for t in range(0, sample - lag):
                    k += px[t] * np.log(px[t] / py[t + lag])

            else:
                for t in range(-lag, sample):
                    k += px[t] * np.log(px[t] / py[t + lag])

            res.append(k)

            if k == min(map(abs, res)):  # 记录相关系数最大时的延迟阶数
                time_lag = lag

        return min(map(abs, res))[0], time_lag

    kl_result = pd.DataFrame(index=data_hp_norm.columns, columns=["klMin", "klPosition"])
    for i in data_hp_norm.columns:
        minKL, KL_lag = kl_info(rs_hp_norm, data_hp_norm[i], sample=n, lag_num=tl)
        kl_result.loc[i, "klMin"] = minKL
        kl_result.loc[i, "klPosition"] = KL_lag

    return kl_result


def standard_sym_change_rate(leadingGroup, coincidentGroup, laggingGroup):
    # 初始化
    C_leading = pd.DataFrame(index=leadingGroup.index, columns=[leadingGroup.columns])
    C_coin = pd.DataFrame(index=coincidentGroup.index, columns=[coincidentGroup.columns])
    C_lagging = pd.DataFrame(index=laggingGroup.index, columns=[laggingGroup.columns])

    # 求对称变化率C
    for i in range(0, C_leading.shape[1]):
        C_leading.iloc[:, i] = 200 * ((leadingGroup.fillna(method="bfill").iloc[:, i].diff()) / (
            leadingGroup.fillna(method="bfill").iloc[:, i].rolling(2).sum()))
    for i in range(0, C_coin.shape[1]):
        C_coin.iloc[:, i] = 200 * ((coincidentGroup.fillna(method="bfill").iloc[:, i].diff()) / (
            coincidentGroup.fillna(method="bfill").iloc[:, i].rolling(2).sum()))
    for i in range(0, C_lagging.shape[1]):
        C_lagging.iloc[:, i] = 200 * ((laggingGroup.fillna(method="bfill").iloc[:, i].diff()) / (
            laggingGroup.fillna(method="bfill").iloc[:, i].rolling(2).sum()))

    # 求标准化因子A
    A_leading = np.abs(C_leading).sum() / (len(leadingGroup) - 1)
    A_coin = np.abs(C_coin).sum() / (len(coincidentGroup) - 1)
    A_lagging = np.abs(C_lagging).sum() / (len(laggingGroup) - 1)

    # 用A将C标准化，得到标准化变化率S
    S_leading = C_leading / A_leading
    S_coin = C_coin / A_coin
    S_lagging = C_lagging / A_lagging

    return S_leading, S_coin, S_lagging, A_leading, A_coin, A_lagging


def standard_mean_change_rate(weight_leading, S_leading, weight_coin, S_coin, weight_lagging, S_lagging):
    # 计算先行、一致、滞后指标组的平均变化率R
    R_leading = S_leading.mul(weight_leading, axis=1).sum(axis=1) / np.sum(weight_leading)
    R_coin = S_coin.mul(weight_coin, axis=1).sum(axis=1) / np.sum(weight_coin)
    R_lagging = S_lagging.mul(weight_lagging, axis=1).sum(axis=1) / np.sum(weight_lagging)

    # 计算指数标准化因子F
    F_leading = (np.sum(np.abs(R_leading[1:]) / (R_leading.shape[0] - 1))) / (
        np.sum(np.abs(R_coin[1:]) / (R_coin.shape[0] - 1)))
    F_coin = (np.sum(np.abs(R_coin[1:]) / (R_coin.shape[0] - 1))) / (np.sum(np.abs(R_coin[1:]) / (R_coin.shape[0] - 1)))
    F_lagging = (np.sum(np.abs(R_lagging[1:]) / (R_lagging.shape[0] - 1))) / (
        np.sum(np.abs(R_coin[1:]) / (R_coin.shape[0] - 1)))

    # 计算标准化平均变化率V
    V_leading = R_leading / F_leading
    V_coin = R_coin / F_coin
    V_lagging = R_lagging / F_lagging

    return V_leading, V_coin, V_lagging


def init_composite_index(V_leading, V_coin, V_lagging):
    """

    :param V_leading:
    :param V_coin:
    :param V_lagging:
    :return:
    """

    # 结构初始化
    I_leading = pd.DataFrame(index=V_leading.index, columns=["I_leading"])
    I_coin = pd.DataFrame(index=V_coin.index, columns=["I_coin"])
    I_lagging = pd.DataFrame(index=V_lagging.index, columns=["I_lagging"])

    # 初始化第一个值
    I_leading.iloc[0] = 100
    I_coin.iloc[0] = 100
    I_lagging.iloc[0] = 100

    # 计算初始合成指数I
    for i in range(1, len(I_leading)):
        I_leading.iloc[i] = I_leading.iloc[i - 1] * ((200 + V_leading[i]) / (200 - V_leading[i]))
    for i in range(1, len(I_coin)):
        I_coin.iloc[i] = I_coin.iloc[i - 1] * ((200 + V_coin[i]) / (200 - V_coin[i]))
    for i in range(1, len(I_lagging)):
        I_lagging.iloc[i] = I_lagging.iloc[i - 1] * ((200 + V_lagging[i]) / (200 - V_lagging[i]))

    return I_leading, I_coin, I_lagging


def firststep_index_analysis(analysis_id, datasource="statistic"):
    """
    第一步模型分析：
        1. 从数据源读取数据（csv数据，数据库数据：景气指标、参考指标）
        2. 对数据进行预处理（同比转换，缺值填补）
        3. 对数据进行季节调整、频度转换
        4. 景气指标与参考指标的转折点匹配
        5. K-L信息量，时差相关系数计算
        6. 第一步分析结果（K-L、时差相关系数）导出到数据库中
        7. 第一步分析的中间计算结果（转折点匹配结果）导出到数据库中
    :param analysis_id: 根据任务id每次分析
    :param datasource: 数据源说明（statistic/ss_result）
    :return: 无具体返回结果，第一步分析的临时结果存库
    """

    # 1. 从数据源读取数据（csv数据，数据库数据：景气指标、参考指标）
    # 2. 对数据进行预处理（同比转换，缺值填补）
    def read_statistic_data_process(filepath, note_colname="标注", indicator_colname="指标"):
        """
        将数据进行变量名转换，并将宽数据转换为长数据
        :param filepath:数据文件路径
        :param note_colname:note的列名
        :param indicator_colname:indicator的列名
        :return:长数据(DataFrame格式)
        """
        rawdata = pd.read_excel(filepath, sheet_name=3, thousands=",")

        rawdata2 = rawdata.rename(columns={note_colname: "note", indicator_colname: "indicator"})

        Long_data = pd.melt(rawdata2, id_vars=["note", "indicator"])
        Long_data[['time']] = Long_data[['variable']].apply(date_parse)
        Long_data2 = Long_data.set_index("time").sort_index()
        Long_data2["indicators"] = Long_data2["note"] + "_" + Long_data2["indicator"]

        return Long_data2

    # 只纳入统计局数据源指标组
    if datasource.lower() == "statistic":

        # 统计局数据读取
        Stat_Data = read_statistic_data_process("./data/input/CSV_Data_Month_All.xlsx", note_colname="标注", indicator_colname="指标")
        start_year = pd.Series(Stat_Data.index).dt.year[0]

        # 统计局数据累计指标处理
        accu_process_result = accumulation_process(Long_df=Stat_Data, note_class="当月累计值")
        accu_var_proc_result = variable_process(accu_process_result, "(后)当月同比", "%", split_str1="_", split_str2="(")

        # 统计局数据同比指标处理
        rate_data = Stat_Data[Stat_Data["note"] == "当月同比"]
        rate_var_proc_result = variable_process(rate_data, "当月同比", False, split_str1="_", split_str2="(")

        # 统计局数据参考指标处理
        refer_data = Stat_Data[Stat_Data["note"] == "参考指标"]
        data_rs_stack = variable_process(refer_data, "参考指标", "%", split_str1="_", split_str2="(")
        data_rs_stack = data_rs_stack.drop(data_rs_stack.index[pd.Series(data_rs_stack.index).dt.year == start_year])

        # 统计局数据结果整理合并
        data_all_stack = pd.concat([accu_var_proc_result, rate_var_proc_result]).sort_index()
        data_all_stack = data_all_stack.drop(data_all_stack.index[pd.Series(data_all_stack.index).dt.year == start_year])

    # 只纳入ss_result数据源指标组
    elif datasource.lower() == "ss_result":

        # 数据库数据读取
        SS_Result = pd.read_csv("./data/input/ssProjectData.csv")
        # sql = 'select * from index_ss_result_data'
        # conn = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/ruoyi')
        # SS_Result = pd.read_sql(sql, conn)

        # 参考指标从csv中读取
        Stat_Data = read_statistic_data_process("../data/input/Data_Month_ALL.xlsx", note_colname="标注", indicator_colname="指标")
        refer_data = Stat_Data[Stat_Data["note"] == "参考指标"]
        data_rs_stack = variable_process(refer_data, "参考指标", "%", split_str1="_", split_str2="(")
        # 数据库数据处理
        data_all_stack = ss_result_process(SS_Result, "INDEX_NAME", "INDEX_VALUE", "YEAR_MONTH", split_str="$")

    # 同时分析两个数据源作为一个整体指标组
    else:
        # 1. 统计局数据读取
        Stat_Data = read_statistic_data_process("./data/input/CSV_Data_Month_All.xlsx", note_colname="标注", indicator_colname="指标")
        start_year = pd.Series(Stat_Data.index).dt.year[0]

        # 统计局数据累计指标处理
        accu_process_result = accumulation_process(Long_df=Stat_Data, note_class="当月累计值")
        accu_var_proc_result = variable_process(accu_process_result, "[Statistical_Bureau]", "%", split_str1="_", split_str2="(")

        # 统计局数据同比指标处理
        rate_data = Stat_Data[Stat_Data["note"] == "当月同比"]
        rate_var_proc_result = variable_process(rate_data, "[Statistical_Bureau]", False, split_str1="_", split_str2="(")

        # 统计局数据参考指标处理
        refer_data = Stat_Data[Stat_Data["note"] == "参考指标"]
        data_rs_stack = variable_process(refer_data, "参考指标", "%", split_str1="_", split_str2="(")
        data_rs_stack = data_rs_stack.drop(data_rs_stack.index[pd.Series(data_rs_stack.index).dt.year == start_year])

        # 统计局数据结果整理合并
        data_all_stack = pd.concat([accu_var_proc_result, rate_var_proc_result]).sort_index()
        data_all_stack1 = data_all_stack.drop(data_all_stack.index[pd.Series(data_all_stack.index).dt.year == start_year])

        # 2. 数据库数据读取
        # SS_Result = input_ss_result("./data/input/SS_Result_Test.xls")
        SS_Result = pd.read_csv("./data/input/ssProjectData.csv")
        # sql = 'select * from index_ss_result_data'
        # conn = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/ruoyi')
        # SS_Result = pd.read_sql(sql, conn)

        # 数据库数据处理
        data_all_stack2 = ss_result_process(SS_Result, "INDEX_NAME", "INDEX_VALUE", "YEAR_MONTH", split_str="$")

        data_all_stack = pd.concat([data_all_stack1, data_all_stack2])
        data_all_stack.index.name = "time"

    data_all = data_all_stack.reset_index().pivot("time", ["note", "subject", "measure"], "value")
    data_rs = data_rs_stack.reset_index().pivot("time", ["note", "subject", "measure"], "value")

    # print(data_all)
    # 3. 对数据进行季节调整、频度转换
    data_hp_norm, rs_hp_norm = data_transform(data_rs, data_all)

    # 取参考指标数据与景气指标数据共有时间段的数据
    join_Data = rs_hp_norm.join(data_hp_norm, how="inner").fillna(method="ffill").fillna(method="bfill")
    rs_hp_norm = join_Data[rs_hp_norm.columns]
    rs_hp_norm.index.name = "time"
    data_hp_norm = join_Data[data_hp_norm.columns]
    rs_hp_norm.index.name = "time"

    # 4. 景气指标与参考指标的转折点匹配
    tpd_extord, tpd_time, tpd_missing, tpd_missingearly, tpd_extra, rs_tp, data_tp = turning_point_deal(rs_hp_norm,
                                                                                                        data_hp_norm)
    tpd_extord.loc[:, "analysis_id"] = analysis_id
    tpd_time.loc[:, "analysis_id"] = analysis_id
    tpd_missing.loc[:, "analysis_id"] = analysis_id
    tpd_missingearly.loc[:, "analysis_id"] = analysis_id
    tpd_extra.loc[:, "analysis_id"] = analysis_id
    rs_tp.loc[:, "analysis_id"] = analysis_id
    data_tp.loc[:, "analysis_id"] = analysis_id

    # 5. K - L信息量，时差相关系数计算
    kl_result = kl_info_compute(data_hp_norm, rs_hp_norm, n=None, tl=12)
    data_totalEval, _, _ = cif.pipelineEvaluation(df1=rs_hp_norm, df2=data_hp_norm,
                                                  missing=tpd_missing, missingEarly=tpd_missingearly,
                                                  extra=tpd_extra, time=tpd_time)

    # 评估指标合并
    Eval_join = kl_result.join(data_totalEval.drop("total", axis=1)).reset_index()
    Eval_join.loc[:, "analysis_id"] = analysis_id
    eval_result = Eval_join[["analysis_id","index",  "klMin", "klPosition", "corrMax", "corrPosition"]]
    eval_result['id'] = None
    eval_resul1 = eval_result.rename(columns={"analysis_id": "analysis_id",
                                              "index": "index_name",
                                              "klMin": "kl_value",
                                              "klPosition": "kl_lag",
                                              "corrMax": "ratio_value",
                                              "corrPosition": "ratio_lag"})

    try:
        # 6. 第一步分析结果（K - L、时差相关系数）导出到数据库中
        conn = create_engine('mysql+pymysql://root:root@localhost:3306/ruoyi')
        eval_resul1.to_sql('index_analysis_detail_data', conn, if_exists='append', index=False)
        print(eval_result.shape)
        data_all_stack.to_sql('data_all_stack', conn, if_exists='replace', index=True)
        data_rs_stack.to_sql('data_rs_stack', conn, if_exists='replace', index=True)
        # print(data_all_stack.shape)

        # 7. 第一步分析的中间计算结果（转折点匹配结果）导出到数据库中
        eval_resul1.to_csv("eval_result.csv", encoding="utf_8_sig", index=True)
        data_rs_stack.to_csv("data_rs_stack.csv", encoding="utf_8_sig", index=True)
        data_all_stack.to_csv("data_all_stack.csv", encoding="utf_8_sig", index=True)
        data_hp_norm.to_csv("data_hp_norm.csv", encoding="utf_8_sig", index=True)
        rs_hp_norm.to_csv("rs_hp_norm.csv", encoding="utf_8_sig", index=True)
        tpd_extord.to_csv("tpd_extord.csv", encoding="utf_8_sig", index=True)
        tpd_time.to_csv("tpd_time.csv", encoding="utf_8_sig", index=True)
        tpd_missing.to_csv("tpd_missing.csv", encoding="utf_8_sig", index=True)
        tpd_missingearly.to_csv("tpd_missingearly.csv", encoding="utf_8_sig", index=True)
        tpd_extra.to_csv("tpd_extra.csv", encoding="utf_8_sig", index=True)
        rs_tp.to_csv("rs_tp.csv", encoding="utf_8_sig", index=True)
        data_tp.to_csv("data_tp.csv", encoding="utf_8_sig", index=True)

        return data_all_stack
        # conn2 = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/ruoyi')
        # data_rs_stack.to_sql('data_rs_stack', conn2, if_exists='replace', index=True)
        # data_all_stack.to_sql('data_all_stack', conn2, if_exists='replace', index=True)
        #
        # data_hp_norm.to_sql('data_hp_norm', conn2, if_exists='replace', index=True)
        # rs_hp_norm.to_sql('rs_hp_norm', conn2, if_exists='replace', index=True)
        # tpd_extord.to_sql('tpd_extord', conn2, if_exists='replace', index=True)
        # tpd_time.to_sql('tpd_time', conn2, if_exists='replace', index=True)
        # tpd_missing.to_sql('tpd_missing', conn2, if_exists='replace', index=True)
        # tpd_missingearly.to_sql('tpd_missingearly', conn2, if_exists='replace', index=True)
        # tpd_extra.to_sql('tpd_extra', conn2, if_exists='replace', index=True)
        # rs_tp.to_sql('rs_tp', conn2, if_exists='replace', index=True)
        # data_tp.to_sql('data_tp', conn2, if_exists='replace', index=True)

    except Exception:
        print('Evaluate Result export to database failed!')
        raise


def secondstep_index_analysis(id, choose_id):
    """
    根据选择的指标和权重进行合成指数：
        1. 从数据库读取数据（选取的指标和权重、第一步计算结果）
        2. 对景气指标进行分组（先行、一致、滞后）
        3. 合成初始的三个指数
        4. 进行趋势调整，合成最终的三个指数
        5. 合成指数结果导出到数据库
    :param choose_id:
    :param task_id:根据任务id来选择第一次计算结果数据
    :return:将最终的合成指数返回到数据库
    """

    # 1. 从数据库读取数据（选取的指标和权重、第一步计算结果）
    def read_choose_result_data(id, choose_id):
        # 连接数据库 index_choose_detail_data/choose_result_data
        sql1 = "select * from index_choose_detail_data where choose_id={}".format(choose_id)
        conn = create_engine('mysql+pymysql://root:root@localhost:3306/ruoyi')

        index_choose = pd.read_sql(sql1, conn)
        index_choose = index_choose.rename(columns={"index_name":"INDEX_NAME",
                                                    "index_type_value":"CHOOSE_CLASS",
                                                    "index_qz_value":"WEIGHT_VALUE"})

        index_choose.loc[index_choose["CHOOSE_CLASS"] == "0", "groupIndicator"] = "LeadingGroup"
        index_choose.loc[index_choose["CHOOSE_CLASS"] == "1", "groupIndicator"] = "CoincidentGroup"
        index_choose.loc[index_choose["CHOOSE_CLASS"] == "2", "groupIndicator"] = "LaggingGroup"

        index_choose.drop(["id"],axis=1).replace(True)
        index_choose["weight"] = index_choose.groupby('groupIndicator')["WEIGHT_VALUE"].apply(lambda x: (x / x.sum()))
        choose_eval_data = index_choose.copy()

        # # 根据权重值分类指标名
        # xx_index = index_choose.loc[index_choose["xx_value"] != 0, "index_name"]
        # yz_index = index_choose.loc[index_choose["yz_value"] != 0, "index_name"]
        # zh_index = index_choose.loc[index_choose["zh_value"] != 0, "index_name"]

        # # 创建分类变量标签
        # choose_eval_data = index_choose.copy()
        # choose_eval_data.loc[choose_eval_data["index_name"].isin(xx_index), "groupIndicator"] = "LeadingGroup"
        # choose_eval_data.loc[choose_eval_data["index_name"].isin(yz_index), "groupIndicator"] = "CoincidentGroup"
        # choose_eval_data.loc[choose_eval_data["index_name"].isin(zh_index), "groupIndicator"] = "LaggingGroup"

        return choose_eval_data

    def read_first_result():

        # conn2 = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/ruoyi')
        # sql1 = "select * from data_hp_norm"
        # sql2 = "select * from rs_hp_norm"
        # sql3 = "select * from tpd_extOrd where task_id={}".format(task_id)
        # sql4 = "select * from tpd_time where task_id={}".format(task_id)
        # sql5 = "select * from tpd_missing where task_id={}".format(task_id)
        # sql6 = "select * from tpd_missingEarly where task_id={}".format(task_id)
        # sql7 = "select * from tpd_extra where task_id={}".format(task_id)
        # sql8 = "select * from rs_tp where task_id={}".format(task_id)
        # sql9 = "select * from data_tp where task_id={}".format(task_id)
        # data_hp_norm = pd.read_sql(sql1, conn2).set_index("time")
        # rs_hp_norm = pd.read_sql(sql2, conn2).set_index("time")
        # tpd_extOrd = pd.read_sql(sql3, conn2).set_index("time")
        # tpd_time = pd.read_sql(sql4, conn2).set_index("time")
        # tpd_missing = pd.read_sql(sql5, conn2).set_index("time")
        # tpd_missingEarly = pd.read_sql(sql6, conn2).set_index("time")
        # tpd_extra = pd.read_sql(sql7, conn2).set_index("time")
        # rs_tp = pd.read_sql(sql8, conn2).set_index("time")
        # data_tp = pd.read_sql(sql9, conn2).set_index("time")

        data_hp_norm = pd.read_csv("data_hp_norm.csv", encoding="utf_8_sig", index_col="time", parse_dates=["time"])
        rs_hp_norm = pd.read_csv("rs_hp_norm.csv", encoding="utf_8_sig", index_col="time", parse_dates=["time"])
        tpd_extOrd = pd.read_csv("tpd_extOrd.csv", encoding="utf_8_sig", index_col="time", parse_dates=["time"])
        tpd_time = pd.read_csv("tpd_time.csv", encoding="utf_8_sig", index_col="time", parse_dates=["time"])
        tpd_missing = pd.read_csv("tpd_missing.csv", encoding="utf_8_sig", index_col="time", parse_dates=["time"])
        tpd_missingEarly = pd.read_csv("tpd_missingEarly.csv", encoding="utf_8_sig", index_col="time", parse_dates=["time"])
        tpd_extra = pd.read_csv("tpd_extra.csv", encoding="utf_8_sig", index_col="time", parse_dates=["time"])
        rs_tp = pd.read_csv("rs_tp.csv", encoding="utf_8_sig", index_col="time", parse_dates=["time"])
        data_tp = pd.read_csv("data_tp.csv", encoding="utf_8_sig", index_col="time", parse_dates=["time"])

        return data_hp_norm, rs_hp_norm, tpd_extOrd, tpd_time, tpd_missing, tpd_missingEarly, tpd_extra, rs_tp, data_tp

    choose_eval_data = read_choose_result_data(id=id, choose_id=choose_id)

    [data_hp_norm, rs_hp_norm, tpd_extOrd, tpd_time,
     tpd_missing, tpd_missingEarly, tpd_extra, rs_tp, data_tp] = read_first_result()

    # 2. 对景气指标进行分组（先行、一致、滞后）
    def split_group(choose_eval_data, data_hp_norm):
        # 选取先行指标组
        leadIndex = choose_eval_data.loc[choose_eval_data["groupIndicator"] == "LeadingGroup", "INDEX_NAME"]
        leadingGroup = data_hp_norm.loc[:, leadIndex]
        # 选取一致指标组
        coinIndex = choose_eval_data.loc[choose_eval_data["groupIndicator"] == "CoincidentGroup", "INDEX_NAME"].values
        coincidentGroup = data_hp_norm.loc[:, coinIndex]
        # 选取滞后指标组
        lagIndex = choose_eval_data.loc[choose_eval_data["groupIndicator"] == "LaggingGroup", "INDEX_NAME"].values

        laggingGroup = data_hp_norm.loc[:, lagIndex]

        return leadIndex, coinIndex, lagIndex, leadingGroup, coincidentGroup, laggingGroup

    [_leadIndex, coinIndex, _lagIndex, leadingGroup, coincidentGroup, laggingGroup] = split_group(choose_eval_data, data_hp_norm)

    # 3. 合成初始的三个指数
    def init_index_composite(choose_eval_data, leadingGroup, coincidentGroup, laggingGroup):
        S_leading, S_coin, S_lagging, A_leading, A_coin, A_lagging = standard_sym_change_rate(leadingGroup,
                                                                                              coincidentGroup,
                                                                                              laggingGroup)

        # 获取选取的指标权重
        w_leading = choose_eval_data.loc[choose_eval_data["groupIndicator"] == "LeadingGroup", "weight"].tolist()
        w_coin = choose_eval_data.loc[choose_eval_data["groupIndicator"] == "CoincidentGroup", "weight"].tolist()
        w_lagging = choose_eval_data.loc[choose_eval_data["groupIndicator"] == "LaggingGroup", "weight"].tolist()

        V_leading, V_coin, V_lagging = standard_mean_change_rate(w_leading, S_leading, w_coin, S_coin, w_lagging,
                                                                 S_lagging)
        I_leading, I_coin, I_lagging = init_composite_index(V_leading, V_coin, V_lagging)

        return V_leading, V_coin, V_lagging, I_leading, I_coin, I_lagging

    V_leading, V_coin, V_lagging, I_leading, I_coin, I_lagging = init_index_composite(choose_eval_data,
                                                                                      leadingGroup,
                                                                                      coincidentGroup,
                                                                                      laggingGroup)

    # 4. 进行趋势调整，合成最终的三个指数
    def last_index_composite(V_leading, V_coin, V_lagging,
                             I_leading, I_coin, I_lagging,
                             data_tp, coinIndex, coincidentGroup):
        # 初始合成指数的转折点检测
        init_leading_tp = cif.pipelineTPDetection(I_leading, printDetails=False, showPlots=False, savePlots=False)
        init_coin_tp = cif.pipelineTPDetection(I_coin, printDetails=False, showPlots=False, savePlots=False)
        init_lagging_tp = cif.pipelineTPDetection(I_lagging, printDetails=False, showPlots=False, savePlots=False)

        def interest_formula(df, dfGroup):
            """
            复利公式：对初始合成指数进行趋势调整

            :param df: 转折点匹配数据集
            :param dfGroup: 指数组
            :return:
            """

            # 初始化
            mI, mL, m = {}, {}, {}
            index_m, c_index1, c_index2, c_index3, c_index4 = {}, {}, {}, {}, {}
            CI, CL, r = {}, {}, {}

            # 时间索引处理
            def months(str1, str2):
                """计算月份差"""
                year1 = str1.year
                year2 = str2.year
                month1 = str1.month
                month2 = str2.month
                num = (year1 - year2) * 12 + (month1 - month2)
                return num

            # 循环组内每个指标
            for ii in df.columns:
                # if index_m[ii].values is None:
                #     continue
                # 指标峰谷的索引

                index_m[ii] = df[ii][(df[ii] != 0)].dropna().index

                # 计算第i个指标最先循环的月数
                mI[ii] = months(index_m[ii][1], index_m[ii][0])
                # 计算第i个指标最后循环的月数
                mL[ii] = months(index_m[ii][len(index_m[ii]) - 1], index_m[ii][len(index_m[ii]) - 2])
                # 计算第i个指标最先循环到最后循环中心的月数
                m[ii] = months(index_m[ii][len(index_m[ii]) - 2] + pd.DateOffset(n=int(mL[ii] / 2), months=1),
                               index_m[ii][0] + pd.DateOffset(n=int(mI[ii] / 2), months=1))

                # 返回序列的最后循环的两个索引位置
                c_index1[ii] = np.where(df[ii].index == index_m[ii][-1])[0][0]
                c_index2[ii] = np.where(df[ii].index == index_m[ii][-2])[0][0]

                # 返回序列的最先循环的两个索引位置
                c_index3[ii] = np.where(df[ii].index == index_m[ii][1])[0][0]
                c_index4[ii] = np.where(df[ii].index == index_m[ii][0])[0][0]

                # 计算CL、CI
                CL[ii] = dfGroup[c_index2[ii]:c_index1[ii]][ii].sum() / mL[ii]
                CI[ii] = dfGroup[c_index4[ii]:c_index3[ii]][ii].sum() / mI[ii]

                # 复利计算公式
                r[ii] = (np.power((CL[ii] + 0.000000001) / (CI[ii] + 0.000000001),
                                  (1 + 0.01) / (m[ii] + 0.01)) - 1) * 100

            return pd.Series(r)

        # 计算一致指标组的平均增长率（目标趋势）Gr
        coin_ri = interest_formula(data_tp.loc[:, coinIndex], coincidentGroup)

        Gr = coin_ri.mean()
        # 对先行、一致、滞后的初始合成指数分别用复利公式计算出各自的平均增长率r
        leading_ri = interest_formula(init_leading_tp, I_leading)

        coin_ri = interest_formula(init_coin_tp, I_coin)

        lagging_ri = interest_formula(init_lagging_tp, I_lagging)

        # 分别对三个指标组的标准化平均变化率作趋势调整V2
        V2_leading = V_leading + (Gr - leading_ri).values
        V2_coin = V_coin + (Gr - coin_ri).values
        V2_lagging = V_lagging + (Gr - lagging_ri).values

        def computeCLI(V2_leading, V2_coin, V2_lagging):
            """
            :param V2_leading:
            :param V2_coin:
            :param V2_lagging:
            :return:
            """

            # 数据结构初始化
            I2_leading = pd.DataFrame(index=V2_leading.index, columns=["I2_leading"])
            I2_coin = pd.DataFrame(index=V2_coin.index, columns=["I2_coin"])
            I2_lagging = pd.DataFrame(index=V2_lagging.index, columns=["I2_lagging"])

            # 第一个值初始化
            I2_leading.iloc[0] = 100
            I2_coin.iloc[0] = 100
            I2_lagging.iloc[0] = 100

            # 计算I2
            for i in range(1, len(I2_leading)):
                I2_leading.iloc[i] = I2_leading.iloc[i - 1] * ((200 + V2_leading[i]) / (200 - V2_leading[i]))
            for i in range(1, len(I2_coin)):
                I2_coin.iloc[i] = I2_coin.iloc[i - 1] * ((200 + V2_coin[i]) / (200 - V2_coin[i]))
            for i in range(1, len(I2_lagging)):
                I2_lagging.iloc[i] = I2_lagging.iloc[i - 1] * ((200 + V2_lagging[i]) / (200 - V2_lagging[i]))

            # 制成以基准年份为100的合成指数CI
            leadingCLI = (I2_leading / I2_leading.mean()) * 100
            coincidentCLI = (I2_coin / I2_coin.mean()) * 100
            laggingCLI = (I2_lagging / I2_lagging.mean()) * 100

            return leadingCLI, coincidentCLI, laggingCLI

        leadingCLI, coincidentCLI, laggingCLI = computeCLI(V2_leading, V2_coin, V2_lagging)

        return leadingCLI, coincidentCLI, laggingCLI

    leadingCLI, coincidentCLI, laggingCLI = last_index_composite(V_leading, V_coin, V_lagging,
                                                                 I_leading, I_coin, I_lagging,
                                                                 data_hp_norm,
                                                                 coinIndex, coincidentGroup)
    leadingCLI["choose_id"] = choose_id
    coincidentCLI["choose_id"] = choose_id
    laggingCLI["choose_id"] = choose_id

    leadingCLI["id"] = None
    coincidentCLI["id"] = None
    laggingCLI["id"] = None

    # 结果可视化
    # plt.plot(coincidentCLI["I2_coin"], label="coincidentCLI")
    # plt.plot(leadingCLI["I2_leading"], label="leadingCLI")
    # plt.plot(laggingCLI["I2_lagging"], label="laggingCLI")
    # plt.legend(loc="best")
    # plt.xlabel("DateTime")
    # plt.ylabel("Index")
    # plt.title("Climate index model")
    # plt.show()

    # 5. 合成指数结果导出到数据库
    # conn = create_engine('mysql+pymysql://root:elane123@172.20.10.9:3306/ruoyi')
    conn = create_engine('mysql+pymysql://root:root@localhost:3306/ruoyi')

    leadingCLI.to_sql('leadingindex_analysis_result', conn, if_exists='append', index=True)
    coincidentCLI.to_sql('coincidentindex_analysis_result', conn, if_exists='append', index=True)
    laggingCLI.to_sql('laggingindex_analysis_result', conn, if_exists='append', index=True)

    # return leadingCLI, coincidentCLI, laggingCLI

if __name__ == '__main__':
    id = 1
    taskid = 1
    chooseid = 1

    # 1 第一步分析：将计算的评价标准写入数据库(中间计算结果存为临时csv)
    firststep_index_analysis(taskid, datasource="statistic")  # ss_result/statistic

    # 2 第二步分析：读取选择的指标和相应权重，结果存库
    secondstep_index_analysis(id, taskid)


