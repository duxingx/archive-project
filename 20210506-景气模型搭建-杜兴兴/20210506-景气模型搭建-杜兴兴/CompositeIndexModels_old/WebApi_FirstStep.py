# -*- coding:utf-8 -*-

import threading
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import tornado.ioloop
import tornado.web
import tornado.gen
import json
import traceback
import mysql.connector
from sqlalchemy import create_engine

from IndexModel import firststep_index_analysis


def main():
    # 读取数据库中的分析id
    # sql1 = "select * from index_analysis_data order by id desc limit 1"
    # conn = create_engine('mysql+pymysql://root:root@localhost:3306/ruoyi')
    # analysis_id_data = pd.read_sql(sql1, conn)
    # analysis_id = analysis_id_data.loc[:, "id"].values[0]

    try:
        # 1 返回”正在执行“执行状态

        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="ruoyi")

        mycursor = mydb.cursor()
        sql = "INSERT INTO `index_analysis_data`( `statistics_count`, `ss_count`, `year_month`, `create_time`) VALUES ('{}', '{}', '{}', NOW())".format(
            0, 0, "202001")
        mycursor.execute(sql)
        analysis_id = mycursor.lastrowid
        print('"指标处理分析"正在执行:', analysis_id)
        mydb.commit()

        # 2 第一步分析结果
        data_all_stack = firststep_index_analysis(analysis_id, datasource="both")
        statistics_count = len(data_all_stack.loc[data_all_stack["note"] == "[Statistical_Bureau]", "subject"].unique())
        ss_count = len(data_all_stack.loc[data_all_stack["note"] == "[SS_Result]", "subject"].unique())
        print(statistics_count)
        print(ss_count)

        # 3 返回”执行完成“执行状态

        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="ruoyi")
        mycursor = mydb.cursor()
        sql = "UPDATE `index_analysis_data` SET `statistics_count`='{}', `ss_count`={}, `status`=3, `status_messg`='{}',`status_time`=now() WHERE `id`='{}'".format(
            statistics_count, ss_count, None, analysis_id)
        mycursor.execute(sql)
        mydb.commit()
        print('"指标处理分析"执行完成:', analysis_id)

    except Exception:
        # 1 返回”执行失败“执行状态
        print('"指标处理分析"执行失败:', analysis_id)
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="ruoyi")
        mycursor = mydb.cursor()
        sql = "UPDATE `index_analysis_data` SET `status`=2, `status_messg`='{}',`status_time`=now() WHERE `id`='{}'".format(
            traceback.format_exc(), analysis_id)
        mycursor.execute(sql)
        mydb.commit()

        # 2 返回异常信息
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        # update task set state='执行异常',remake='traceback.format_exc()' where task_id=task_id;


class Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("主方法")
        main()


poolexecutor = ThreadPoolExecutor(max_workers=8)


class MainHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    @tornado.gen.coroutine
    def get(self):
        """post接口， 获取参数"""
        thread = Thread()
        thread.start()
        poolexecutor.submit(thread)
        self.write(json.dumps({'code': 200}))


application = tornado.web.Application([(r"/doTask", MainHandler), ])

if __name__ == "__main__":
    application.listen(8001)
    tornado.ioloop.IOLoop.instance().start()
