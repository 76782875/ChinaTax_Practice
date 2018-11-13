# -*- coding: utf-8 -*-
# 文件名称: conversion_data.py
# 作者: JianNoo
# 创建日期: 2018-10-06
# 功能描述: 将SQLServer数据去重后转换成Sqlite数据
# 网址: 12366.chinatax.gov.cn/BsdtAllBLH_bsdtMain.do#
# 完成状况：完成

import pymysql
import sqlite3
import os
from ChinaTax import settings
import pandas as pd
import json


class Conversion(object):
    def __init__(self):
        self.__config = {  # 从settings文件获取数据库连接配置信息
            'host': settings.MYSQL_HOST,
            'port': settings.MYSQL_PORT,
            'username': settings.MYSQL_USER,
            'password': settings.MYSQL_PASSWORD,
            'database': settings.MYSQL_DBNAME,
            'charset': settings.MYSQL_CHARSET
        }
        self.path = os.path.dirname(os.path.abspath(__file__)) + '\Data'  # 数据存储路径

    def get_id(self):
        with open("id.json", 'r') as file:  # 获取json文件中的id
            id_data = json.loads(file.read())
        return id_data

    def create_folder(self):  # 创建文件夹，存储sqlite数据库
        # 判断路径是否存在
        isExists = os.path.exists(self.path)
        if not isExists:
            # 如果不存在则创建目录
            os.makedirs(self.path)

    def connect_mysql(self):
        db = pymysql.connect(  # 连接数据库
            host=self.__config['host'],
            port=self.__config['port'],
            user=self.__config['username'],
            passwd=self.__config['password'],
            db=self.__config['database'],
            charset=self.__config['charset']
        )
        return db

    def storage_data(self, province_name, city_name):
        db = self.connect_mysql()  # 获取数据库对象
        # sql查询语句
        sql = "SELECT province, city, name, address, phone, longitude, latitude, officeHours FROM `%s` WHERE city = '%s'" % (province_name, city_name)
        df = pd.read_sql(sql, db)  # 使用pandas获取数据
        df1 = df.drop_duplicates()  # 去重
        path = self.path + '\\' + province_name + '.db'  # Sqlite数据库存储路径
        conn = sqlite3.connect(path)  # 创建sqlite数据库
        df1.to_sql(province_name, conn, 'sqlite', if_exists='append', index=False)  # 将数据存储进Sqlite
        db.close()  # 关闭数据库
        conn.close()  # 关闭数据库

    def main(self):  # 主函数
        self.create_folder()  # 创建文件夹
        id_data = self.get_id()  # 获取id
        for item in id_data:  # 循环转换数据
            for province_name, city_data in item.items():
                for city in city_data:
                    for city_name, city_id in city.items():
                        self.storage_data(province_name, city_name)


def Conversion_main():
    Conversion().main()


if __name__ == '__main__':
    Conversion_main()
