# -*- coding:utf-8 -*-
import sys
from pylab import *
import matplotlib.pyplot as plt
reload(sys)
sys.setdefaultencoding('utf-8')
mpl.rcParams['font.sans-serif'] = ['SimHei']

labels = u'C语言', u'数据库', u'嵌入式', u'Linux', u'Python', u'Windows', u'Java'
fracs = [25, 23, 22, 15, 5, 5, 5]
explode = [0.1, 0, 0, 0, 0, 0, 0]
patches,l_text,p_text = plt.pie(fracs,explode=explode,labels=labels,
                                labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
                                startangle = 90,pctdistance = 0.6)
for t in l_text:
    t.set_size=(30)
for t in p_text:
    t.set_size=(20)
plt.axis('equal')
plt.legend()
plt.title(u'岗位能力需求图谱')
plt.show()