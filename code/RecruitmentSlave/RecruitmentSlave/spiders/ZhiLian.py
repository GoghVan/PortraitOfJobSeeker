# -*- coding: utf-8 -*-
# @Time    : 2018/5/21 18:12
# @Author  : Gavin

import urllib
import json
import scrapy
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisSpider
from RecruitmentSlave.items import ZhiLianItem
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger("ZhiLianSlaveSpider")


class ZhiLianSlaveSpider(RedisSpider):
    name = 'ZhiLian'
    redis_key = 'ZhiLianCrawl:requests'
    allowed_domains = ['xiaoyuan.zhaopin.com']
    custom_settings = {
        # 'ITEM_PIPELINES': {'RecruitmentSlave.pipelines.ZhiLianPipeline': 300},
        'DOWNLOAD_DELAY': 1,
        'DOWNLOAD_TIMEOUT': 10,
        'RETRY_TIMES': 2,
    }

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "lxml", from_encoding='utf-9')
        companyid = soup.find('input', type='hidden', id="hidden_jobuser")['companyid']
        subcompanyid = soup.find('input', type='hidden', id="hidden_jobuser")['subcompanyid']

        node_list = response.xpath('/html/body/div[@class="cRecruiterIndex_Wrap cRecruiterWrap"]'
                                   '/div[@class="cWrap"]/div[@class="cMain"]/div/div/div')
        item = ZhiLianItem()
        item['position_link'] = ''  # response.meta['url']
        item['position_name'] = node_list[0].xpath('./div/h1/text()').extract()[0].strip()  # 职位名称
        item['company_name'] = node_list[0].xpath('./div/ul/li/a/text()').extract()[0]  # 公司名称
        item['position_location'] = node_list[0].xpath('./div/ul[2]/li[@id="currentJobCity"]/@title').extract()[0]  # 工作地点
        item['release_date'] = node_list[0].xpath('./div/ul[2]/li[@id="liJobPublishDate"]/text()').extract()[0]  # 发布日期
        item['position_number'] = node_list[0].xpath('./div/ul[2]/li[6]/text()').extract()[0]  # 招聘人数
        item['position_type'] = node_list[0].xpath('./div/ul[2]/li[4]/text()').extract()[0]  # 职位类型
        item['position_information'] = node_list[0].xpath('./div[2]/div[2]/div[1]/div[1]/p[1]').xpath('string(.)').extract()[0].strip()  # 职位信息
        item['company_scale'] = node_list[0].xpath('./div/ul/li[@class="cJobDetailInforWd2"]/text()')
        if len(item['company_scale']) == 2:
            item['company_scale'] = item['company_scale'].extract()[1]  # 公司规模
        else:
            item['company_scale'] = ''
        item['company_type'] = node_list[0].xpath('./div/ul[1]/li/text()').extract()[-1]  # 公司类型
        item['company_business'] = node_list[0].xpath('./div/ul/li[@class="cJobDetailInforWd2"]/text()').extract()[
            0]  # 公司行业
        item['company_homepage'] = ''
        item['company_adress'] = ''
        # 判断右侧
        if len(node_list) != 1:
            tip = node_list[1].xpath('./div[@class="cRightTab mt20"]/h4/span/text()').extract()
            if len(tip) == 0:
                item['company_homepage'] = node_list[1].xpath('./div[@class="cRightTab mt20"]/div/p/a/text()')  # 公司主页
                if len(item['company_homepage']) == 0:
                    item['company_homepage'] = ''
                else:
                    item['company_homepage'] = item['company_homepage'].extract()[0]
                item['company_adress'] = node_list[1].xpath('./div[@class="cRightTab mt20"]/div/p/text()').extract()[
                    0].strip()  # 公司地址
            else:
                item['company_homepage'] = ''
                item['company_adress'] = ''
        url = 'https://xiaoyuan.zhaopin.com/jobdetail/GetCompanyIntro/' + companyid \
              + '?subcompanyid=' + subcompanyid + '&showtype=1'
        yield scrapy.Request(url, meta={'item': item}, callback=self.first_parse, dont_filter=True)

    def first_parse(self, response):
        item = response.meta['item']
        data = response.body
        item['company_information'] = ''
        if len(data) != 39861:
            item['company_information'] = urllib.unquote(str(json.loads(data)['intro'])).replace('<strong>', '')\
                .replace('</strong>', '').replace('<br/>', '').replace('<br>', '').replace(' ', '')\
                .replace('\n', '').strip()
        yield item
