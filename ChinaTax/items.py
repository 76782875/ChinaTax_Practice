# -*- coding: utf-8 -*-
# 文件名称: items.py
# 作者: JianNoo
# 创建日期: 2018-10-06
# 功能描述: 从非结构性的数据源提取结构性数据
# 网址: 12366.chinatax.gov.cn/BsdtAllBLH_bsdtMain.do#
# 完成状况：完成
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class ChinataxItem(scrapy.Item):
    # define the fields for your item here like:
    province_name = scrapy.Field()  # 省份名称
    city = scrapy.Field()  # 城市/区名称
    name = scrapy.Field()  # 名称
    address = scrapy.Field()  # 地址
    phone = scrapy.Field()  # 电话
    longitude = scrapy.Field()  # 经度
    latitude = scrapy.Field()  # 纬度
    officeHours = scrapy.Field()  # 办公时间

