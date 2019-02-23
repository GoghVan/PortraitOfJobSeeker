# -*- coding:utf-8 -*-
from collections import Counter
import jieba.analyse
import xlwt

wbk = xlwt.Workbook(encoding='ascii')
sheet = wbk.add_sheet("wordCount")  # Excel单元格名字
word_lst = []
key_list = []
bill_path = r'job2.txt'
bill_result_path = r'job2_result.txt'
car_path = 'car.txt'
with open(bill_path,'r') as fr:
        data = jieba.cut(fr.read())
data = dict(Counter(data))
with open(bill_result_path,'w') as fw:
    for k,v in data.items():
        fw.write("%s,%d\n" % (k.encode('utf-8'),v))