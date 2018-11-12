# -*- coding: utf-8 -*-
# 文件名称: main.py
# 作者: FengJianBo
# 创建日期: 2018-10-06
# 功能描述: 调试scrapy爬虫
# 网址: 12366.chinatax.gov.cn/BsdtAllBLH_bsdtMain.do#
# 完成状况：完成

from scrapy.cmdline import execute
import os
import sys


def main():  # 主函数
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 进入当前项目所在位置
    execute(['scrapy', 'crawl', 'chinatax'])  # 执行爬虫


if __name__ == '__main__':
    main()
