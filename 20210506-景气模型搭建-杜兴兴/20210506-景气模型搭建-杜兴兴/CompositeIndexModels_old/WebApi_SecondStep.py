# _*_ encoding:utf-8 _*_

# -*- coding:utf-8 -*-

import threading
from concurrent.futures import ThreadPoolExecutor
import tornado.ioloop
import tornado.web
import tornado.gen
import json
import traceback
import mysql.connector

from IndexModel import secondstep_index_analysis


def main(id=1, choose_id=1):
    try:
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="ruoyi")
        sqlinsert="INSERT INTO `ruoyi`.`index_task_info`(`choose_id`, `create_time`) VALUES ('{}', NOW());".format(choose_id)
        mycursor = mydb.cursor()
        mycursor.execute(sqlinsert)
        id = mycursor.lastrowid
        mydb.commit()
        # 1 返回”正在执行“执行状态
        print('"选择指标任务"正在执行:', id, choose_id)

        # mycursor = mydb.cursor()
        # sql = "UPDATE `index_task_info` SET `status`=1, `status_messg`=NULL, `status_time`=now() WHERE `id`= '{}' and `choose_id`='{}'".format(id,choose_id)
        # mycursor.execute(sql)


        # 2 第二步分析结果
        secondstep_index_analysis(id, choose_id)

        # 3 返回”执行完成“执行状态
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="ruoyi")
        mycursor = mydb.cursor()
        sql = "UPDATE `index_task_info` SET `status`=3, `status_messg`='{}',`status_time`=now() WHERE `id`= '{}' and `choose_id`='{}'".format(None, id, choose_id)
        mycursor.execute(sql)
        mydb.commit()
        print('"指标处理分析"执行完成:', id, choose_id)

    except Exception:
        # 1 返回”执行失败“执行状态
        print('"选择指标任务"执行失败:', id, choose_id)
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="ruoyi")
        mycursor = mydb.cursor()
        sql = "UPDATE `index_task_info` SET `status`=2, `status_messg`={},`status_time`=now() WHERE `id`= '{}' and `choose_id`='{}'".format(traceback.format_exc(), id, choose_id)
        mycursor.execute(sql)
        mydb.commit()

        # 2 返回异常信息
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        # update task set state='执行异常',remake='traceback.format_exc()' where task_id=task_id;


class Thread(threading.Thread):
    def __init__(self, id, choose_id):
        threading.Thread.__init__(self)
        self.choose_id = choose_id
        self.id = id

    def run(self):
        print("获取到的参数", self.id, self.choose_id)
        main(self.id, self.choose_id)


poolexecutor = ThreadPoolExecutor(max_workers=8)


class MainHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    @tornado.gen.coroutine
    def get(self):
        """post接口， 获取参数"""
        # id = self.get_argument("id")
        choose_id = self.get_argument("choose_id")
        thread = Thread(0, choose_id)
        thread.start()
        poolexecutor.submit(thread)
        self.write(json.dumps({'code': 200, 'result': choose_id}))


application = tornado.web.Application([(r"/doTask", MainHandler), ])

if __name__ == "__main__":
    application.listen(8002)
    tornado.ioloop.IOLoop.instance().start()
