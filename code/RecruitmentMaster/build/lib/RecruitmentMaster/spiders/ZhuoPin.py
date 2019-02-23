# -*- coding: utf-8 -*-
# @Time    : 2018/5/21 14:27
# @Author  : Gavin
import scrapy
import logging
from bs4 import BeautifulSoup
from scrapy.conf import settings
from RecruitmentMaster.src.InsertRedis import InsertRequest
import sys
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger("ZhuoPinMasterSpider")


class ZhuoPinMasterSpider(scrapy.Spider):
    # 名称
    name = 'ZhuoPin'
    # 域名
    allowed_domains = ['www.highpin.cn']
    # 初始化url
    start_urls = ['http://www.highpin.cn/zhiwei/all.html']
    # 不同行业
    industries = settings['ZHUOHPIN_INDUSTRYCELLS']
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 10,
        'DOWNLOAD_DELAY': 1,
        'RETRY_TIMES': 2,
    }

    def parse(self, response):
        for industry in self.industries:
            url = 'http://www.highpin.cn/zhiwei/ci_' + industry + '.html'
            yield scrapy.Request(url, callback=self.first_parse)

    def first_parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "lxml", from_encoding='utf-9')
        cururl = soup.find('a', id='stitle')['href'][:-5] + '_p_'
        page = int(soup.find_all('a', class_='c-page sign')[-1].string) + 1
        for num in range(1, page):
            url = cururl + str(num) + '.html'
            yield scrapy.Request(url, callback=self.second_parse)

    @staticmethod
    def second_parse(response):
        data = response.body
        soup = BeautifulSoup(data, "lxml", from_encoding='utf-9')
        # 每页所有连接
        contents = soup.find_all('div', class_='jobInfoItem clearfix bor-bottom add-bg')
        for content in contents:
            href = content.find('div', class_='clearfix').find('div', class_='c-list-search c-wid320 align-l') \
                .find('p', class_='jobname clearfix').find('a')
            url = 'http://www.highpin.cn' + href['href']
            InsertRequest(url, 1)
            logger.info("ZhuoPinMasterSpiderUrl: %s" % url)
