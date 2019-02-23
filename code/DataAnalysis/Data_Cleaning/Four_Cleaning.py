# -*- coding: utf-8 -*-
# @Time    : 2018/6/10 15:31
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
    sheetname_1 = dbname['data_three']
    sheetname_2 = dbname['data_four']

    # data = sheetname.find_one()
    datas = sheetname_1.find()
    for data in datas:
        data.pop('_id')
        data.pop('position_major')
        data.pop('work_experience')
        data.pop('position_allday')
        data.pop('position_apartment')
        data.pop('position_number')
        data.pop('position_age')
        data.pop('position_language')
        data.pop('release_date')
        data.pop('position_salary')
        data.pop('position_education')

        sheetname_2.insert(data)

if __name__ == "__main__":
    process_item()