# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ZhiLianItem(Item):
    # 职位名称
    position_name = Field()
    # 职位链接
    position_link = Field()
    # 公司名称
    company_name = Field()
    # 工作地点
    position_location = Field()
    # 发布日期
    release_date = Field()
    # 招聘人数
    position_number = Field()
    # 职位类型
    position_type = Field()
    # 职位信息
    position_information = Field()
    # 公司介绍
    company_information = Field()
    # 公司规模
    company_scale = Field()
    # 公司类型
    company_type = Field()
    # 公司行业
    company_business = Field()
    # 公司主页
    company_homepage = Field()
    # 公司地址
    company_adress = Field()


class ZhuoPinItem(Item):
    # 职位名称
    position_name = Field()
    # 公司名称
    company_name = Field()
    # 公司福利
    company_treatment = Field()
    # 职位薪酬
    position_salary = Field()
    # 工作地点
    position_location = Field()
    # 发布日期
    release_date = Field()
    # 工作经验
    work_experience = Field()
    # 学历要求
    position_education = Field()
    # 年龄要求
    position_age = Field()
    # 海外经历
    position_overseas = Field()     # 上有下没有
    # 招聘人数
    position_number = Field()
    # 职位类型
    position_type = Field()
    # 所属部门
    position_apartment = Field()
    # 专业要求
    position_major = Field()
    # 语言要求
    position_language = Field()
    # 招全日制
    position_allday = Field()
    # 职位信息
    position_information = Field()
    # 公司介绍
    company_information = Field()
    # 公司规模
    company_scale = Field()
    # 公司类型
    company_type = Field()
    # 公司行业
    company_bussiness = Field()
    # 公司地址
    company_address = Field()   # 上有下没有
    # 招聘url
    web_url = Field()


class BossItem(Item):
    # 职位名称
    position_name = Field()
    # 公司介绍
    company_information = Field()
    # 工作经验
    work_experience = Field()
    # 职位薪酬
    position_salary = Field()
    # 工作城市
    work_city = Field()
    # 学历要求
    position_education = Field()
    # 公司名称
    company_name = Field()
    # 公司行业
    company_bussiness = Field()
    # 经济规模
    company_finance = Field()
    # 公司规模
    company_scale = Field()
    # 发布时间
    release_date = Field()
    # 工作地点
    position_location = Field()
    # 招聘url
    web_url = Field()
    # 职位信息
    position_information = Field()
    # 公司主页
    company_homepage = Field()


class ChinaHRItem(Item):
    position_name = Field()
    position_location = Field()
    position_require = Field()
    position_salary = Field()
    company_treatment = Field()
    position_information = Field()
    position_type = Field()
    company_type = Field()
    company_service = Field()
    crawled = Field()
    spider = Field()
