# -*- coding: utf-8 -*-
# 文件名称: pipelines.py
# 作者: JianNoo
# 创建日期: 2018-10-06
# 功能描述: 将数据异步存储进数据库
# 网址: 12366.chinatax.gov.cn/BsdtAllBLH_bsdtMain.do#
# 完成状况：完成

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import os
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi
import copy


class MysqlTwistPipeline(object):  # 异步

    @classmethod
    def from_settings(cls, settings):  # 使用scrapy内置函数获取数据库配置信息
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset=settings['MYSQL_CHARSET'],
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
            )
        # 这是链接数据库的另一种方法，在settings中写入参数
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)  # 异步
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        # 使用twiest将mysql插入变成异步
        asynItem = copy.deepcopy(item)
        # 使用异步时，需要使用copy的深度复制，不然数据会重复，原因是twiest框架的执行顺序是从上往下，等执行到最后时，数据已经变了
        query = self.dbpool.runInteraction(self.do_insert, asynItem)
        # 因为异步 可能有些错误不能及时爆出
        query.addErrback(self.handle_error)
        return item

    # 处理异步的异常
    def handle_error(self,failure):
        print('failure')

    def do_insert(self, cursor, item):
        # sql语句
        insert_sql = """INSERT INTO `%s`(province, city, name, address, phone, longitude, latitude, officeHours)
                                VALUES('%s','%s','%s', '%s', '%s', '%s', '%s', '%s')
                        """ % (
        item['province_name'], item['province_name'], item['city'], item['name'], item['address'], item['phone'],
        item['longitude'], item['latitude'], item['officeHours'])
        cursor.execute(insert_sql)  # 执行sql语句
        return item


# class MysqlPipeline(object):  # 同步
#
#     def __init__(self):
          # 连接数据库
#         self.conn = pymysql.connect('localhost', 'root', 'root', 'db_chinatax', charset='utf8', use_unicode=True)
#         self.cursor = self.conn.cursor()  # 获取游标
#
#     def process_item(self, item, spider):  # 执行数据插入
#         insert_sql = """INSERT INTO `%s`(province, city, name, address, phone, longitude, latitude, officeHours)
#                         VALUES('%s','%s','%s', '%s', '%s', '%s', '%s', '%s')
#                 """ % (item['province_name'], item['province_name'], item['city'], item['name'], item['address'], item['phone'], item['longitude'], item['latitude'], item['officeHours'])
#         self.cursor.execute(insert_sql)  # 执行sql语句
#         self.conn.commit()  # 提交sql语句
#         return item
