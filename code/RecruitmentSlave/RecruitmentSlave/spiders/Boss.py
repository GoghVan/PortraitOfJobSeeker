# -*- coding: utf-8 -*-
# @Time    : 2018/5/21 18:12
# @Author  : Gavin
import sys
import scrapy
import logging
from scrapy_redis.spiders import RedisSpider
from RecruitmentSlave.items import BossItem
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger("BossSlaveSpider")


class BossSlaveSpider(RedisSpider):
    name = 'Boss'
    redis_key = 'BossCrawl:requests'
    allowed_domains = ['www.zhipin.com']
    custom_settings = {
        # 'ITEM_PIPELINES': {'RecruitmentSlave.pipelines.BossPipeline': 300},
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
            'RecruitmentSlave.middlewares.HttpProxyMiddleware': 543,
        },
        'DOWNLOAD_TIMEOUT': 10,
        'DOWNLOAD_DELAY': 2,
        'RETRY_TIMES': 0,
    }

    def parse(self, response):
        contents = response.xpath("//*[@id='main']/div/div[2]/ul/li")
        for each in contents:
            item = BossItem()
            item["position_name"] = each.xpath("./div/div[1]/h3/a/div[1]/text()").extract()[0]
            item["position_salary"] = each.xpath("./div/div[1]/h3/a/span/text()").extract()[0]
            item['web_url'] = 'https://www.zhipin.com' + each.xpath("./div/div[1]/h3/a/@href").extract()[0]
            info_primary = each.xpath("./div/div[1]/p/text()").extract()
            item["work_city"] = info_primary[0]
            item["work_experience"] = info_primary[1]
            item["position_education"] = info_primary[2]
            item["company_name"] = each.xpath("./div/div[2]/div/h3/a/text()").extract()[0]
            company_infos = each.xpath("./div/div[2]/div/p/text()").extract()
            item["company_bussiness"] = ''
            item["company_finance"] = ''
            item["company_scale"] = ''
            if len(company_infos) == 3:
                item["company_bussiness"] = company_infos[0]
                item["company_finance"] = company_infos[1]
                item["company_scale"] = company_infos[2]
            item["release_date"] = each.xpath("./div/div[3]/p/text()").extract()[0]
            yield scrapy.Request(item['web_url'], meta={'item': item}, callback=self.first_parse, dont_filter=True)

    def first_parse(self, response):
        item = response.meta['item']
        contents = response.xpath('//body')
        item['position_information'] = contents.xpath('//*[@id="main"]/div[3]/div/div[2]/div[3]/div[1]/div').xpath('string(.)').extract()[0].strip()
        item['position_location'] = contents.xpath('//div[@class="location-address"]/text()').extract()[0].strip()
        item['company_information'] = contents.xpath('//div[@class="job-sec company-info"]/div').xpath('string(.)').extract()
        if len(item['company_information']) != 0:
            item['company_information'] = item['company_information'][0].strip()
        else:
            item['company_information'] = ''
        item['company_homepage'] = contents.xpath('//div[@class="info-company"]/p[2]/text()').extract()
        if len(item['company_homepage']) != 0:
            item['company_homepage'] = item['company_homepage'][0].strip()
        else:
            item['company_homepage'] = ''
        yield item
