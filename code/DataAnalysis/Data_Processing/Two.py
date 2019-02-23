# -*- coding: utf-8 -*-
# @Time    : 2018/6/10 18:18
# @Author  : Gavin

from __future__ import division
import pymongo
import sys
import jieba
from pylab import mpl
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
reload(sys)
sys.setdefaultencoding('utf-8')

type1 = ['IT/互联网/通信/电子', '互联网', '移动互联网', '电子商务', '计算机软件', 'IT服务', '电子技术', '半导体', '集成电路', '计算机硬件', '网络设备', '通信', '电信']
type2 = ['金融', '金融', '银行', '投资', '基金', '证券', '期货', '保险']
type3 = ['房地产/建筑', '房地产', '建筑', '建材', '工程', '家居', '室内设计', '装饰装潢', '物业管理', '商业中心']
type4 = ['商业服务', '专业服务', '中介服务', '外包服务', '检验', '检测', '认证']
type5 = ['造纸及纸制品/印刷', '印刷', '包装', '造纸']
type6 = ['贸易消费品/批发零售', '快速消费品', '耐用消费品', '贸易', '进出口', '零售', '批发']
type7 = ['加工制造/仪表设备', '汽车', '摩托车', '大型设备', '机电设备', '重工业', '加工制造', '仪器仪表', '工业自动化', '航空', '航天研究与制造']
type8 = ['交通/运输/物流', '交通', '运输', '物流']
type9 = ['制药/生物/医疗/保健', '医药', '生物工程', '医疗', '护理', '美容','保健', '卫生服务', '医疗设备', '器械']
type10 = ['教育/培训', '教育', '培训', '院校']
type11 = ['酒店/餐饮/旅游/休闲', '酒店', '餐饮', '旅游', '度假', '娱乐', '体育', '休闲']
type12 = ['广告/传媒', '媒体', '出版', '影视', '文化传播', '广告', '会展', '公关', '市场推广']
type13 = ['能源/电气/化工/环保', '石油', '石化', '化工', '能源', '矿产', '采掘', '冶炼', '电气', '电力', '水利', '环保']
type14 = ['政府/非盈利机构', '学术', '科研', '政府', '公共事业', '非盈利机构']
type15 = ['农林牧渔', '农', '林', '牧', '渔']
type16 = ['其他', '租赁服务', '其他']
type_all = [type1, type2, type3, type4, type5, type6, type7, type8, type9,
            type10, type11, type12, type13, type14, type15, type16]

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
    company_bussiness = {}
    count = 0
    string = ''
    for data in datas:
        if '/' in data['company_bussiness']:
            bussiness = str(data['company_bussiness']).split('/')
            for bus in bussiness:
                string = string + bus
                if bus not in company_bussiness:
                    company_bussiness[bus] = 1
                else:
                    company_bussiness[bus] = company_bussiness[bus] + 1
                count = count + 1
    company_bussiness = sorted(company_bussiness.items(), key=lambda d: d[1], reverse=True)
    bussiness = {}
    for other in company_bussiness:
        for types in type_all:
            if other[0] in types[1:]:
                if types[0] not in bussiness:
                    bussiness[types[0]] = other[1]
                else:
                    bussiness[types[0]] = bussiness[types[0]] + other[1]
                break
    company_bussiness = sorted(bussiness.items(), key=lambda d: d[1], reverse=True)
    return company_bussiness, string, count


def bussiness_num_ciyun():
    # C:\Windows\Fonts\STXINGKA.TTF
    path_img = "F:\SoftProgram\pycharm\DataAnalysis\src\\back1.jpg"
    company_bussiness, string, count = process_item()
    path_of_font = "C:\Windows\Fonts\STXINWEI.TTF"
    background_image = np.array(Image.open(path_img))
    wordlist_after_jieba = jieba.cut(string, cut_all=False)
    wl_space_split = " ".join(wordlist_after_jieba)
    my_wordcloud = WordCloud(
        font_path=path_of_font,
        background_color="white",
        # width=1000,
        # height=880,
        mask=background_image,
    ).generate(wl_space_split)
    image_colors = ImageColorGenerator(background_image)
    plt.imshow(my_wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.imshow(my_wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def bussiness_num_pie():
    bussiness_num, string, count = process_item()
    labels = [x[0] for x in bussiness_num]
    sizes = [x[1]/count*100 for x in bussiness_num]
    explode = [0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    plt.axes(aspect=1)
    plt.pie(x=sizes, explode=explode, colors=color, labels=labels, autopct='%3.1f%%', shadow=False,
            labeldistance=1.1, startangle=0, pctdistance=0.8, center=(-1, 0))
    plt.legend(loc=7, bbox_to_anchor=(1, 1), ncol=3, fancybox=True, shadow=True, fontsize=8)
    plt.axis('equal')
    plt.show()


def bussiness_num_bar():
    bussiness_num, string, count = process_item()
    labels = [x[0] for x in bussiness_num]
    sizes = [x[1] / count * 100 for x in bussiness_num]
    plt.xlabel(u"公司性质")
    plt.xticks(rotation=30)
    plt.ylabel(u"性质百分比")
    plt.title(u"公司性质所占百分比")
    rect1 = plt.bar(range(len(sizes)), sizes, color=color, tick_label=labels)
    for rect in rect1:
        height = round(rect.get_height(), 3)
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height) + '%', ha="center", va="bottom")
    plt.legend(handles=rect1, labels=labels, loc='best')
    plt.show()


if __name__ == "__main__":
    bussiness_num_bar()

