# -*- coding: utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def get_json():
    f = open('news.json', 'r')
    for line in f.readlines():
        setting = json.loads(line)
        new = json.dumps(setting, ensure_ascii=False)
        news = setting['position_name']
        t = '软件工程师'
        if t in news:
            w = open('job2.txt', 'a+')
            x = setting['position_information']
            w.write(x)
            w.close()
        # new = json.dumps(setting,ensure_ascii=False)
    f.close()
t = get_json()

print(t)