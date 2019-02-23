# -*- coding: utf-8 -*-
# @Time    : 2018/6/4 10:29
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
    sheetname_1 = dbname['zhuopin']
    sheetname_2 = dbname['data_one']

    # data = sheetname.find_one()
    datas = sheetname_1.find()
    for data in datas:
        data.pop('_id')
        data.pop('web_url')
        data.pop('company_address')
        data.pop('position_overseas')
        if len(str(data['company_treatment'])) == 0:
            data['company_treatment'] = '无'
        data_len = len(data.keys())
        for key in data.keys():
            if len(str(data[key])) != 0:
                if data_len == 1:
                    sheetname_2.insert(data)
                data_len = data_len - 1
if __name__ == "__main__":
    process_item()