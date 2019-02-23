# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys
import logging
import codecs
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger("Pipelines")


class ZhiLianPipeline(object):
    def __init__(self):
        self.file = codecs.open('F:\SoftProgram\pycharm\data\zhilian.json', 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        spider.logger.info('ZhiLianPipeline: %s' % line)

    def spider_closed(self, spider):
        self.file.close()


class ZhuoPinPipeline(object):
    def __init__(self):
        self.file = codecs.open('F:\SoftProgram\pycharm\data\zhuopin.json', 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        spider.logger.info('ZhuoPinPipeline: %s' % line)

    def spider_closed(self, spider):
        self.file.close()


class BossPipeline(object):
    def __init__(self):
        self.file = codecs.open('F:\SoftProgram\pycharm\data\\boss.json', 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        spider.logger.info('BossPipeline: %s' % line)

    def spider_closed(self, spider):
        self.file.close()


class ChinaHRPipeline(object):
    def __init__(self):
        self.file = codecs.open('F:\SoftProgram\pycharm\data\\chinahr.json', 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        spider.logger.info('ChinaHRPipeline: %s' % line)

    def spider_closed(self, spider):
        self.file.close()
