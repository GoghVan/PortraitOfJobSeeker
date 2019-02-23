# -*- coding: utf-8 -*-
# @Time    : 2018/6/4 20:00
# @Author  : Gavin
import re
import json
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
    sheetname_1 = dbname['data_two']
    sheetname_2 = dbname['data_three']
    # 查找数据
    datas = sheetname_1.find()
    patten1 = re.compile(r'（.*?）|\(.*?\)')
    patten2 = re.compile(r'、|及|＋|,')
    patten3 = re.compile(r',')
    patten4 = re.compile(r'-其他')
    patten5 = re.compile(r'支持-|支持/')
    patten6 = re.compile(r'、|，|或')
    patten7 = re.compile(r'相关专业|及相关|\.\.\.|类相关专业|类|相关|专业')
    patten8 = re.compile(r'以下|以上|及以上')
    patten9 = re.compile(r'\\|、|，|／')

    for data in datas:
        data.pop('_id')
        company_bussiness = re.subn(patten1, '', str(data['company_bussiness']))[0]
        data['company_bussiness'] = re.subn(patten2, '/', company_bussiness)[0]
        position_type = re.subn(patten3, '/', str(data['position_type']))[0]
        position_type = re.subn(patten4, '/其他', position_type)[0]
        data['position_type'] = re.subn(patten5, '', position_type)[0]
        data['position_language'] = str(data['position_language']).replace('：',':').replace('|', '/')
        position_major = str(data['position_major']).replace('None', '不限')
        position_major = re.subn(patten6, '/', position_major)[0]
        data['position_major'] = re.subn(patten7, '', position_major)[0]
        data['position_location'] = str(data['position_location']).replace(',', '/')
        data['position_age'] = str(data['position_age']).replace('从', '').replace('岁到', '-')
        data['company_scale'] = re.subn(patten8, '', str(data['company_scale']))[0]
        data['work_experience'] = re.subn(patten8, '', str(data['work_experience']))[0]
        position_name = str(data['position_name']).replace('（', '(').replace('）', ')').replace('：', '')
        data['position_name'] = re.subn(patten9, '', position_name)[0]
        data = json.dumps(data)
        with open('C:\Users\Gavin\Desktop\\news.json', 'a+') as fd:
            fd.write(data + "\n")
        # sheetname_2.insert(data)

if __name__ == "__main__":
    process_item()