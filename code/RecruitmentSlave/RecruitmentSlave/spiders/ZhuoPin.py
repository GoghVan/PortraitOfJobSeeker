# -*- coding: utf-8 -*-
# @Time    : 2018/5/21 18:12
# @Author  : Gavin
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisSpider
from RecruitmentSlave.items import ZhuoPinItem
import logging
logger = logging.getLogger("ZhuoPinSlaveSpider")


class ZhuoPinSlaveSpider(RedisSpider):
    name = 'ZhuoPin'
    redis_key = 'ZhuoPinCrawl:requests'
    custom_settings = {
        # 'ITEM_PIPELINES': {'RecruitmentSlave.pipelines.ZhuoPinPipeline': 300},
        'DOWNLOAD_DELAY': 1,
        'DOWNLOAD_TIMEOUT': 10,
        'RETRY_TIMES': 2,
    }

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "lxml", from_encoding='utf-8')
        contents = soup.find_all('div', class_='mainContent')
        if len(contents) != 0:
            item = ZhuoPinItem()
            item['web_url'] = ''    # response.meta['web_url']
            item['company_name'] = contents[0].find('a', class_='innerSite_link').get_text(strip=True)
            item['company_name'] = contents[0].find_all('ul')[0].a.string
            item['position_apartment'] = contents[0].find_all('ul')[1].find_all('li')[1]['title']
            item['company_bussiness'] = contents[0].find_all('ul')[0].find_all('span')[2]['title']
            item['company_address'] = contents[0].find_all('ul')[0].find_all('span')[6]['title'].strip()
            item['company_type'] = contents[0].find_all('ul')[0].find_all('li')[2].contents
            if len(item['company_type']) > 1:
                item['company_type'] = item['company_type'][1]
            else:
                item['company_type'] = ''
            company_scale = contents[0].find_all('ul')[0].find_all('li')[3]
            if len(company_scale) >= 2:
                item['company_scale'] = contents[0].find_all('ul')[0].find_all('li')[3].contents[1]
            else:
                item['company_scale'] = ''
            item['position_type'] = contents[0].find_all('ul')[1].find_all('li')[0]['title']  # .split('/')[0]
            item['position_location'] = contents[0].find_all('ul')[1].find_all('li')[2]['title']
            item['release_date'] = contents[0].find_all('ul')[1].find_all('li')[3].contents[3].string
            item['position_number'] = contents[0].find_all('ul')[2].find_all('li')
            if len(item['position_number']) == 3:
                item['position_number'] = item['position_number'][2].contents[1]
            elif len(item['position_number']) == 2:
                item['position_number'] = item['position_number'][1].contents[1]
            elif len(item['position_number']) == 1:
                item['position_number'] = item['position_number'][0].contents[1]
            else:
                item['position_number'] = ''
            item['position_salary'] = contents[0].find_all('ul')[3].a.string
            item['work_experience'] = contents[0].find_all('ul')[4].span.contents[0]
            item['position_education'] = contents[0].find_all('ul')[4].find_all('li')[1].contents[2].strip()
            position_allday = contents[0].find_all('ul')[5]
            if len(position_allday) > 3:
                item['position_allday'] = contents[0].find_all('ul')[5].find_all('li')[1].contents[1]
            else:
                item['position_allday'] = contents[0].find_all('ul')[5].find_all('li')[0].contents[1]

            item['position_age'] = contents[0].find_all('ul')[5].find_all('li')[0].contents[1].strip()
            item['position_information'] = contents[0].find_all('div', class_='v-p-w')[0].get_text(strip=True)
            item['position_overseas'] = contents[0].find_all('p', class_='v-pstyle view-wid490')[0].string
            item['position_major'] = contents[0].find_all('p', class_='v-pstyle view-wid490')[1].string
            item['position_language'] = contents[0].find_all('p', class_='v-pstyle view-wid490')[2].string
            item['company_information'] = contents[0].find_all('p', class_='view-aboutUs v-pstyle txt_indent0')
            if len(item['company_information']) != 0:
                item['company_information'] = item['company_information'][0].get_text(strip=True)
            else:
                item['company_information'] = ''
            contents = soup.find_all('h1', class_='postitonName pl_25')
            item['company_treatment'] = contents[0].find_all('div', class_='labelList lh14 mar-B4 ')
            if len(item['company_treatment']) != 0:
                item['company_treatment'] = item['company_treatment'][0].get_text(strip=True)
            else:
                item['company_treatment'] = ''
            item['position_name'] = contents[0].find_all('span', class_='cursor-d ')[0]['title']
            yield item
        else:
            contents = soup.find_all('div', class_='c-view-box online')
            if len(contents) != 0:
                item = ZhuoPinItem()
                item['web_url'] = ''  # response.meta['web_url']
                item['position_name'] = contents[0].find_all('span', class_='cursor-d')[0]['title']
                item['company_treatment'] = contents[0].find_all('div', class_='labelList lh14 mar-B4')
                if len(item['company_treatment']) != 0:
                    item['company_treatment'] = item['company_treatment'][0].get_text(strip=True)
                else:
                    item['company_treatment'] = ''
                item['company_name'] = contents[0].find_all('ul', class_='view-ul')[0].find_all('li')[0]['title']
                item['company_bussiness'] = contents[0].find_all('ul', class_='view-ul')[0].find_all('li')[1]['title']
                item['company_type'] = contents[0].find_all('ul', class_='view-ul')[0].find_all('li')[2].contents
                if len(item['company_type']) > 1:
                    item['company_type'] = item['company_type'][1]
                else:
                    item['company_type'] = ''
                item['company_scale'] = contents[0].find_all('ul', class_='view-ul')[0].find_all('li')[3].contents[1]
                item['position_type'] = contents[0].find('div', class_='c-view-con').find_all('ul', class_='view-ul view-wid344')[0].find_all('li')[0]['title']
                item['position_apartment'] = contents[0].find('div', class_='c-view-con').find_all('ul', class_='view-ul view-wid344')[0].find_all('li')[1]['title']
                item['position_location'] = contents[0].find('div', class_='c-view-con').find_all('ul', class_='view-ul view-wid344')[0].find_all('li')[2]['title']
                item['release_date'] = contents[0].find('div', class_='c-view-con').find_all('ul', class_='view-ul view-wid344')[0].find_all('li')[3].find_all('span')[1].contents[0]

                item['position_number'] = contents[0].find('div', class_='c-view-con').find_all('ul', class_='view-ul ul-pst1')[0].find_all('li')
                if len(item['position_number']) == 3:
                    item['position_number'] = item['position_number'][2].contents[1]
                elif len(item['position_number']) == 2:
                    item['position_number'] = item['position_number'][1].contents[1]
                elif len(item['position_number']) == 1:
                    item['position_number'] = item['position_number'][0].contents[1]
                else:
                    item['position_number'] = ''
                item['position_salary'] = contents[0].find('div', class_='c-view-con').find_all('li', class_='mar-b8')[0].find_all('span')[1].a.string
                item['position_information'] = ''
                position_information = contents[0].find('div', class_='detail-div fl').find_all('p')
                if len(position_information) != 0:
                    for i in position_information:
                        item['position_information'] = item['position_information'] + i.get_text(strip=True)
                item['work_experience'] = contents[0].find('div', class_='add-div800 clearfix').find_all('ul')[0].find_all('li')[0].find('span').string
                item['position_education'] = contents[0].find('div', class_='add-div800 clearfix').find_all('ul')[0].find_all('li')[1].contents[2].strip()
                item['position_age'] = contents[0].find('div', class_='add-div800 clearfix').find_all('ul')[1].find_all('li')[0].contents[1]
                item['position_allday'] = contents[0].find('div', class_='add-div800 clearfix').find_all('ul')[1].find_all('li')[1].contents[1]
                item['position_major'] = contents[0].find_all('div', class_='clearfix mar-l120')[0].p.string
                item['position_language'] = contents[0].find_all('div', class_='clearfix mar-l120')[1].p.string
                item['company_information'] = contents[0].find_all('p', class_='view-aboutUs v-pstyle txt_indent0')
                if len(item['company_information']) != 0:
                    item['company_information'] = item['company_information'][0].get_text(strip=True)
                else:
                    item['company_information'] = ''
                item['position_overseas'] = ''
                item['company_address'] = ''
                yield item
