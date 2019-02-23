# -*- coding: utf-8 -*-
# @Time    : 2018/6/4 15:12
# @Author  : Gavin


import json
import time
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def process_item():
    # 创建MongoDB数据库链接
    mongodbcli = pymongo.MongoClient(host='127.0.0.1', port=27017)
    # 创建mongodb数据库名称
    dbname = mongodbcli['JobData']
    # 创建mongodb数据库表的名称
    sheetname_1 = dbname['data_one']
    sheetname_2 = dbname['data_two']

    datas = sheetname_1.find()
    for data in datas:
        data.pop('_id')
        for key in data.keys():
            data[key] = str(data[key]).replace(' ', '')
        sheetname_2.insert(data)

if __name__ == "__main__":
    process_item()