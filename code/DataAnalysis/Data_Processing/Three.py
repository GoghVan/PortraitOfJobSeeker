# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 20:05
# @Author  : Gavin
import sys
import pymongo
import re
from pylab import mpl
import matplotlib.pyplot as plt
reload(sys)
sys.setdefaultencoding('utf8')
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
color = ['#9ACD32', '#2E8B57', '#FF6347', '#7FFFD4', '#DA70D6', '#00BFFF', '#FF7F50', '#9400D3', '#A52A2A', '#DEB887',
         '#7FFF00', '#FFC0CB', '#FFD700', '#808080', '#008000', '#20B2AA']


def process_item():
    # 创建MongoDB数据库链接
    mongodbcli = pymongo.MongoClient(host='127.0.0.1', port=27017)
    # 创建mongodb数据库名称
    dbname = mongodbcli['JobData']
    # 创建mongodb数据库表的名称
    sheetname = dbname['data_four']
    # 查找数据
    datas = sheetname.find()
    location_num = {}
    count = 0
    patten1 = re.compile(r'-(.*?)')
    for data in datas:
        if '/' in data['position_location']:
            locations = str(data['position_location']).split('/')
            for location in locations:
                # location = re.subn(patten1, '', str(location))[0]
                location = location.split('-')[0]
                if location not in location_num:
                    location_num[location] = 1
                else:
                    location_num[location] = location_num[location] + 1
                count = count + 1
        else:
            # location = re.subn(patten1, '', str(data['position_location']))[0]
            # location = data['position_location']
            location = str(data['position_location']).split('-')[0]
            if location not in location_num:
                location_num[location] = 1
            else:
                location_num[location] = location_num[location] + 1
            count = count + 1
    location_num = sorted(location_num.items(), key=lambda d: d[1], reverse=True)
    return location_num, count


def location_num_bar():
    location_num, count = process_item()
    labels = [x[0] for x in location_num]
    sizes = [x[1] for x in location_num]
    plt.xlabel(u"公司地址")
    plt.xticks(rotation=30)
    plt.ylabel(u"地区公司数量")
    plt.title(u"公司地址与各地区数量")
    rect1 = plt.bar(range(len(sizes)), sizes, color=color, tick_label=labels)
    for rect in rect1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    plt.legend(handles=rect1, labels=labels, loc='best', ncol=3)
    plt.show()


if __name__ == "__main__":
    location_num_bar()