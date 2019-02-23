# -*- coding: utf-8 -*-
# @Time    : 2018/5/21 14:26
# @Author  : Gavin
import scrapy
import logging
import sys
from RecruitmentMaster.src.InsertRedis import InsertRequest
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger("BossMasterSpider")


class BossMasterSpider(scrapy.Spider):
    name = 'Boss'
    allowed_domains = ['www.zhipin.com']
    curPage = 1
    base_url = 'https://www.zhipin.com'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
            'RecruitmentMaster.middlewares.HttpProxyMiddleware': 543,
        },
        'DOWNLOAD_TIMEOUT': 10,
        'DOWNLOAD_DELAY': 1,
        'RETRY_TIMES': 0,
    }
    start_urls = ['https://www.zhipin.com/']

    def parse(self, response):
        labs = response.xpath('//dl/div[@class="menu-sub"]/ul/li/div/a/@href')
        for lab in labs:
            url = self.base_url + lab.extract()
            for num in range(1, 11):
                job_url = url + ("?page=%d&ka=page-%d" % (num, num))
                InsertRequest(job_url, 2)
                logger.info("BossMasterSpiderUrl: %s" % job_url)
