# -*- coding: utf-8 -*-
# @Time    : 2018/5/21 13:55
# @Author  : Gavin

import scrapy
from RecruitmentMaster.src.InsertRedis import InsertRequest
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger("ZhiLianMasterSpider")


class ZhiLianMasterSpider(scrapy.Spider):
    # 名称
    name = 'ZhiLian'
    # 域名
    allowed_domains = ['xiaoyuan.zhaopin.com']
    # 初始URL
    start_urls = ['https://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_0_1_0']
    # 初始偏移量
    offset = 1
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 10,
        'DOWNLOAD_DELAY': 1,
        'RETRY_TIMES': 2,
    }

    def parse(self, response):
        # 总页数
        total_pages = response.xpath('/html/body/div[@class="wrapper"]/div[@class="searchMain clearfix"]'
                                     '/div[@class="searchMainl fl"]/div/div[@class="searchResultHead clearfix"]'
                                     '/div[@class="searchResultInfo fr"]/span[@class="searchResultPagePer fr"]'
                                     '/text()').extract()[0][1:]
        # 招聘链接
        recruitment_urls = response.xpath('/html/body/div[@class="wrapper"]/div[@class="searchMain clearfix"]'
                                          '/div[@class="searchMainl fl"]/div/div/ul/li'
                                          '/div[@class="searchResultItemDetailed"]/a/@href').extract()
        # 循环遍历每页
        for url in recruitment_urls:
            url = 'https:' + url
            InsertRequest(url, 0)
            logger.info("ZhiLianMasterSpiderUrl: %s" % url)

        # 页数增加
        if self.offset <= total_pages:
            self.offset = self.offset + 1
            url = 'https://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_0_' + str(self.offset) + '_0'
            yield scrapy.Request(url, callback=self.parse)
