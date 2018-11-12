# -*- coding: utf-8 -*-
# 文件名称: create_table.py
# 作者: FengJianBo
# 创建日期: 2018-10-06
# 功能描述: 根据省份创建数据表
# 网址: 12366.chinatax.gov.cn/BsdtAllBLH_bsdtMain.do#
# 完成状况：完成
import pymysql
from ChinaTax import settings


class Create(object):
    def __init__(self):
        self.__config = {  # 从settings文件获取数据库配置信息
            'host': settings.MYSQL_HOST,
            'port': settings.MYSQL_PORT,
            'username': settings.MYSQL_USER,
            'password': settings.MYSQL_PASSWORD,
            'database': settings.MYSQL_DBNAME,
            'charset': settings.MYSQL_CHARSET
        }

    def create_mysql_table(self, province_name):
        db = pymysql.connect(  # 连接数据库
            host=self.__config['host'],
            port=self.__config['port'],
            user=self.__config['username'],
            passwd=self.__config['password'],
            db=self.__config['database'],
            charset=self.__config['charset']
            )
        cursor = db.cursor()
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        cursor.execute("DROP TABLE IF EXISTS {}".format(province_name))
        # 使用预处理语句创建表
        sql = """CREATE TABLE `{}` (
                        `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        `province` varchar(255) DEFAULT NULL,
                        `city` varchar(255) DEFAULT NULL,
                        `name` varchar(255) DEFAULT NULL,
                        `address` varchar(255) DEFAULT NULL,
                        `phone` varchar(255) DEFAULT NULL,
                        `longitude` varchar(255) DEFAULT NULL,
                        `latitude` varchar(255) DEFAULT NULL,
                        `officeHours` varchar(255) DEFAULT NULL
                        )""".format(province_name)
        cursor.execute(sql)  # 执行数据库语句
        db.close()  # 关闭数据库
