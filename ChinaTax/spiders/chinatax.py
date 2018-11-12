# -*- coding: utf-8 -*-
# 文件名称: main.py
# 作者: FengJianBo
# 创建日期: 2018-10-06
# 功能描述: 爬取项目
# 网址: 12366.chinatax.gov.cn/BsdtAllBLH_bsdtMain.do#
# 完成状况：完成
from scrapy import Spider, Request, FormRequest
import json
from ChinaTax.items import ChinataxItem
from ChinaTax.create_table import Create


class ChinataxSpider(Spider):
    name = 'chinatax'  # 爬虫名称
    allowed_domains = ['12366.chinatax.gov.cn/BsdtAllBLH_bsdtMain.do#']
    start_urls = ['http://12366.chinatax.gov.cn/BsdtAllBLH_bsdtMain.do#/']

    def __init__(self):
        self.id_data = []  # 存储id
        self.province_data = {}  # 存储省份名称和id
        self.start_url = 'http://12366.chinatax.gov.cn/BsdtAllBLH_bsdtMain.do#/'  # 起始网址
        self.info_url = 'http://12366.chinatax.gov.cn/BsdtAllBLH_bsdtGetBst.do'  # 信息网址
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'}  # 请求头
        self.cookies = {'acw_tc': '7b39758815372536468094663e1201da6386695d1ee66e4dd4dd6335324876',
                        'acw_sc__v1': 'NWJhOWVjMjIyZTRkYjUyZGE5ZDYwOWJiNDNhNjYzMDIyZmY2YzVlNw==',
                        'JSESSIONID': 'BF4263267553A91731F8A84CD62F9999',
                        'SERVERID': 'ddb0ba16e1611448b580200c17718de3|1537863190|1537862690'
                        }  # cookies

    def start_requests(self):
        yield Request(self.start_url, headers=self.headers, cookies=self.cookies, callback=self.parse_id)  # 请求服务器，获取数据

    def parse_id(self, response):  # 处理数据
        ul = response.xpath('//*[@id="sj-menu"]/li').extract()  # 使用xpath解析数据
        for i in range(2, len(ul)+1):
            province_id = response.xpath('//*[@id="sj-menu"]/li['+str(i)+']/@id').extract_first()  # 提取省份id
            province_name = response.xpath('//*[@id="sj-menu"]/li['+str(i)+']/@name').extract_first()  # 提取省份名称
            self.province_data[province_name] = province_id  # 存储省份信息
            li = response.xpath('//*[@id="sj-menu"]/li['+str(i)+']/a').extract()
            city_data = []
            for k in range(1, len(li)+1):
                # 提取城市id
                city_id = response.xpath('//*[@id="sj-menu"]/li['+str(i)+']/a['+str(k)+']/@id').extract_first()
                city_name = response.xpath('//*[@id="sj-menu"]/li[' + str(i) + ']/a[' + str(k) + ']/text()').extract_first()
                city_data.append({city_name: city_id})
            self.id_data.append({province_name: city_data})  # 按省份形式存储城市id
        with open('id.json', 'w')as file:  # 将提取出来的数据以json方式存进json文件，以便数据转换
            file.write(json.dumps(self.id_data))
        for keys, value in self.province_data.items():
            Create().create_mysql_table(keys)  # 根据省份名称创建数据库和数据表
        if self.id_data:
            for item in self.id_data:
                for province_name, city_data in item.items():  # 使用循环迭代字典，提取省份名称和城市id
                    province_id = self.province_data[province_name]  # 获取省份id
                    for city_info in city_data:
                        for city_name, city_id in city_info.items():
                            from_data = {  # 组装请求数据
                                'sjbh': str(city_id),
                                'sfbh': str(province_id),
                                'lx': '1',
                                'search': ''}
                            yield FormRequest(self.info_url, headers=self.headers, formdata=from_data, callback=self.parse_info, dont_filter=True, meta={'province_name': province_name, 'city_name': city_name})  # 请求服务器，获取数据

    def parse_info(self, response):  # 处理数据
        data = json.loads(response.body)  # 使用json解析数据
        province_name = response.meta['province_name']
        city_name = response.meta['city_name']
        items = ChinataxItem()  # 获取item对象，进行赋值
        if data:
            for item in data:
                items['province_name'] = province_name
                items['city'] = city_name
                items['name'] = item.get('swjgmc', '')
                items['address'] = item.get('swjgdz', '')
                items['phone'] = item.get('swjglxdh', '')
                items['longitude'] = item.get('x', '')
                items['latitude'] = item.get('y', '')
                officeHours = item.get('bssj', '')
                if officeHours:
                    items['officeHours'] = officeHours.replace('\n', ' ').replace('\r', ' ')
                else:
                    items['officeHours'] = officeHours
                yield items  # 返回处理好的数据
