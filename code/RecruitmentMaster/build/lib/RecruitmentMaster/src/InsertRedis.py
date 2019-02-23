# -*- coding: utf-8 -*-
# @Time    : 2018/5/21 14:03
# @Author  : Gavin

import redis
import logging
logger = logging.getLogger('InsertRequest')


def InsertRequest(url, type):
    try:
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        if type == 0:
            r.lpush('ZhiLianCrawl:requests', url)
        if type == 1:
            r.lpush('ZhuoPinCrawl:requests', url)
        if type == 2:
            r.lpush('BossCrawl:requests', url)
        if type == 3:
            r.lpush('ChinaHRCrawl:requests', url)
    except:
        logger.info("Redis open failed!!!")

