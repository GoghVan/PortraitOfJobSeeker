# -*- coding: utf-8 -*-
# @Time    : 2018/6/10 15:12
# @Author  : Gavin
from __future__ import division
import re
import json
import pymongo
import sys
import pygal
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import jieba as jb
from wordcloud import WordCloud
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

reload(sys)
sys.setdefaultencoding('utf8')


def process_item():
    # 创建MongoDB数据库链接
    mongodbcli = pymongo.MongoClient(host='127.0.0.1', port=27017)
    # 创建mongodb数据库名称
    dbname = mongodbcli['JobData']
    # 创建mongodb数据库表的名称
    sheetname = dbname['data_four']
    # 查找数据
    datas = sheetname.find()
    type_num = {}
    count = 0
    for data in datas:
        if data['company_type'] not in type_num:
            types = data['company_type']
            type_num[types] = 1
        else:
            types = data['company_type']
            num = type_num[types] + 1
            type_num[types] = num
        count = count + 1
    type_num = sorted(type_num.items(), key=lambda d: d[1], reverse=True)
    return type_num, count

color = ['#9ACD32', '#2E8B57', '#FF6347', '#7FFFD4', '#DA70D6', '#00BFFF', '#FF7F50', '#9400D3', '#A52A2A', '#DEB887',
         '#7FFF00', '#FFC0CB', '#FFD700', '#808080', '#008000', '#20B2AA']


def type_num_pie():
    type_num, count = process_item()
    labels = [x[0] for x in type_num]
    sizes = [x[1]/count*100 for x in type_num]
    # pie_chart = pygal.Pie(inner_radius=.5)
    # pie_chart.title = 'CompanyType & Percentage'
    # pie_chart.add(labels[0], sizes[0])
    # pie_chart.add(labels[1], sizes[1])
    # pie_chart.add(labels[2], sizes[2])
    # pie_chart.add(labels[3], sizes[3])
    # pie_chart.add(labels[4], sizes[4])
    # pie_chart.add(labels[5], sizes[5])
    # pie_chart.add(labels[6], sizes[6])
    # pie_chart.add(labels[7], sizes[7])
    # pie_chart.add(labels[8], sizes[8])
    # pie_chart.add(labels[9], sizes[9])
    # pie_chart.add(labels[10], sizes[10])
    # pie_chart.add(labels[11], sizes[11])
    # pie_chart.add(labels[12], sizes[12])
    # pie_chart.add(labels[13], sizes[13])
    # pie_chart.add(labels[14], sizes[14])
    # pie_chart.add(labels[15], sizes[15])
    # pie_chart.render_to_file('F:\SoftProgram\pycharm\DataAnalysis\src\type_num_pie.svg')

    # colors = ['yellow', 'green', 'gold', 'lightskyblue', 'lightcoral', 'blue', 'red', 'coral', 'orange']
    explode = [x * 0.05 for x in range(len(type_num))]
    plt.axes(aspect=1)
    plt.pie(x=sizes, explode=explode, colors=color, labels=labels, autopct='%3.1f%%', shadow=False,
            labeldistance=1.1, startangle=0, pctdistance=0.8, center=(-1, 0))
    plt.legend(loc=7, bbox_to_anchor=(1.5, 0.90), ncol=3, fancybox=True, shadow=True, fontsize=8)
    # plt.axis('equal')
    plt.show()


def type_num_bar():
    type_num, count = process_item()
    labels = [x[0] for x in type_num]
    sizes = [x[1] / count * 100 for x in type_num]
    # pie_chart = pygal.HorizontalBar()
    # pie_chart.title = 'CompanyType & Percentage'
    # pie_chart.add(labels[0], sizes[0])
    # pie_chart.add(labels[1], sizes[1])
    # pie_chart.add(labels[2], sizes[2])
    # pie_chart.add(labels[3], sizes[3])
    # pie_chart.add(labels[4], sizes[4])
    # pie_chart.add(labels[5], sizes[5])
    # pie_chart.add(labels[6], sizes[6])
    # pie_chart.add(labels[7], sizes[7])
    # pie_chart.add(labels[8], sizes[8])
    # pie_chart.add(labels[9], sizes[9])
    # pie_chart.add(labels[10], sizes[10])
    # pie_chart.add(labels[11], sizes[11])
    # pie_chart.add(labels[12], sizes[12])
    # pie_chart.add(labels[13], sizes[13])
    # pie_chart.add(labels[14], sizes[14])
    # pie_chart.add(labels[15], sizes[15])
    # pie_chart.render_to_file('F:\SoftProgram\pycharm\DataAnalysis\src\type_num_bar.svg')

    plt.xlabel(u"公司类型")
    plt.ylabel(u"类型百分比")
    plt.title(u"公司类型所占百分比")
    rect1 = plt.bar(range(len(sizes)), sizes, color=color, tick_label=labels)
    for rect in rect1:
        height = round(rect.get_height(), 3)
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height) + '%', ha="center", va="bottom")
    plt.legend(handles=rect1, labels=labels, loc='best')
    plt.show()


if __name__ == "__main__":
    type_num_bar()
