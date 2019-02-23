# -*- coding: utf-8 -*-
# @Time    : 2018/5/21 17:04
# @Author  : Gavin
import sys
import logging
from scrapy import Request
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from RecruitmentMaster.src.InsertRedis import InsertRequest
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger("CinaHRMasterSpider")


class ChinaHRMasterSpider(Spider):
    name = 'ChinaHR'
    allowed_domains = ['www.chinahr.com']
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 10,
        'DOWNLOAD_DELAY': 1,
        'RETRY_TIMES': 2,
    }

    def start_requests(self):
        pages = []
        for i in range(1, 175):
            url = 'http://www.chinahr.com/sou/?orderField=relate&city=17,182&page=%s' % i
            page = Request(url)
            pages.append(page)
        return pages

    def parse(self, response):
        page_content = LinkExtractor(allow="job\/\d+.html")
        links = page_content.extract_links(response)
        for lin in links:
            if lin:
                InsertRequest(lin.url, 3)
                logger.info("CinaHRMasterSpiderUrl: %s" % lin.url)

