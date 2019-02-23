# -*- coding: utf-8 -*-
# @Time    : 2018/5/21 18:12
# @Author  : Gavin
import sys
import logging
from scrapy_redis.spiders import RedisSpider
from RecruitmentSlave.items import ChinaHRItem
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger("ChinaHRSlaveSpider")


class ChinaHRSlave(RedisSpider):
    name = 'ChinaHR'
    redis_key = 'ChinaHRCrawl:requests'
    custom_settings = {
        # 'ITEM_PIPELINES': {'RecruitmentSlave.pipelines.ChinaHRPipeline': 300},
        'DOWNLOAD_TIMEOUT': 10,
        'DOWNLOAD_DELAY': 1,
        'RETRY_TIMES': 2,
    }

    def parse(self, response):
        item = ChinaHRItem()
        item['position_name'] = response.xpath('//div[@class="job-detail  page clear"]/div[@class="job-detail-l"]'
                                               '/div[@class="job_profile jpadding"]/div[@class="base_info"]'
                                               '/div/h1/span[@class="job_name"]/text()').extract_first().strip()
        item['position_location'] = response.xpath('//div[@class="job-detail  page clear"]/div[@class="job-detail-l"]'
                                                   '/div[@class="job_profile jpadding"]/div[@class="base_info"]'
                                                   '/div[@class="job_require"]/span[@class="job_loc"]/text()')\
            .extract_first().strip()
        item['position_salary'] = response.xpath('//div[@class="job-detail  page clear"]/div[@class="job-detail-l"]'
                                                 '/div[@class="job_profile jpadding"]/div[@class="base_info"]'
                                                 '/div[@class="job_require"]/span[@class="job_price"]/text()')\
            .extract_first().strip()
        item['position_require'] = response.xpath('string(//div[@class="job-detail  page clear"]'
                                                  '/div[@class="job-detail-l"]'
                                                  '/div[@class="job_profile jpadding"]/div[@class="base_info"]'
                                                  '/div[@class="job_require"])').extract_first().strip()
        item['company_treatment'] = response.xpath('string(//div[@class="job-detail  page clear"]'
                                                   '/div[@class="job-detail-l"]'
                                                   '/div[@class="job_profile jpadding"]/div[@class="job_fit_tags"]'
                                                   '/ul[@class="clear"])').extract_first().strip()
        item['position_type'] = response.xpath(
            'string(//div[@class="job-detail  page clear"]/div[@class="job-detail-l"]'
            '/div[@class="job_intro jpadding  mt15"]/div[@class="job_intro_tag"])').extract_first().strip()
        item['position_information'] = response.xpath('//div[@class="job-detail  page clear"]'
                                                      '/div[@class="job-detail-l"]'
                                                      '/div[@class="job_intro jpadding  mt15"]'
                                                      '/div[@class="job_intro_wrap"]'
                                                      '/div[@class="job_intro_info"]/text()').extract_first().strip()
        item['company_type'] = response.xpath('string(//div[@class="job-detail  page clear"]/div[@class="job-detail-l"]'
                                              '/div[@class="company_intro  jpadding mt15"]'
                                              '/div[@class="compny_tag"])').extract_first().strip()
        item['company_service'] = response.xpath('//div[@class="job-detail  page clear"]/div[@class="job-detail-l"]'
                                                 '/div[@class="company_intro  jpadding mt15"]'
                                                 '/div[@class="company_service"]/text()').extract_first().strip()
        yield item
