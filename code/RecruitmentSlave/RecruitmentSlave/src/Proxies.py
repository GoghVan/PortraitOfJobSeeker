# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 8:48
# @Author  : Gavin

import re
import urllib2
import logging
from bs4 import BeautifulSoup
import subprocess as sp
logger = logging.getLogger(__name__)


def get_html(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/45.0.2454.99 Safari/537.36'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    html = urllib2.urlopen(request)
    return html.read()


def get_soup(url):
    soup = BeautifulSoup(get_html(url), "lxml")
    return soup


def fetch_xici(https):
    """
    http://www.xicidaili.com/nn/
    """
    proxies = []
    url = "http://www.xicidaili.com/nn/"
    soup = get_soup(url)
    table = soup.find("table", attrs={"id": "ip_list"})
    trs = table.find_all("tr")
    for i in range(1, len(trs)):
        tr = trs[i]
        tds = tr.find_all("td")
        ip = tds[1].text
        port = tds[2].text
        if https and tds[5].text.strip() != "HTTPS":
            continue
        speed = tds[6].div["title"][:-1]
        latency = tds[7].div["title"][:-1]
        if float(speed) < 3 and float(latency) < 1:
            if https:
                proxies.append("https://%s:%s" % (ip, port))
            else:
                proxies.append("http://%s:%s" % (ip, port))
    return proxies


def img2port(img_url):
    """
    mimvp.com的端口号用图片来显示, 本函数将图片url转为端口, 目前的临时性方法并不准确
    """
    code = img_url.split("=")[-1]
    if code.find("AO0OO0O") > 0:
        return 80
    else:
        return None


def fetch_mimvp(https):
    """
    从http://proxy.mimvp.com/free.php抓免费代理
    """
    proxies = []
    if https:
        return proxies
    url = "http://proxy.mimvp.com/free.php?proxy=in_hp"
    soup = get_soup(url)
    table = soup.find("div", class_="free-list")
    tds = table.tbody.find_all("td")
    for i in range(0, len(tds), 10):
        id = tds[i].text
        ip = tds[i + 1].text
        port = img2port(tds[i + 2].img["src"])
        response_time = tds[i + 7]["title"][:-1]
        transport_time = tds[i + 8]["title"][:-1]
        if port is not None and float(response_time) < 1:
            proxy = "http://%s:%s" % (ip, port)
            proxies.append(proxy)
    return proxies


def fetch_66ip(https):
    """
    http://www.66ip.cn/
    每次打开此链接都能得到一批代理, 速度不保证
    """
    proxies = []
    # 修改getnum大小可以一次获取不同数量的代理
    if https:
        url = "http://www.66ip.cn/nmtq.php?getnum=100&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=" \
              "1&proxytype=1&api=66ip"
    else:
        url = "http://www.66ip.cn/nmtq.php?getnum=100&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1" \
              "&proxytype=0&api=66ip"
    content = get_html(url)
    content = str(content)
    urls = content.split("</script>")[3].split("</div>")[0].split("<br />")
    for u in urls:
        u = u.split("\\t")[-1]
        if u.strip():
            if https:
                proxies.append("https://" + u.strip())
            else:
                proxies.append("http://" + u.strip())
    return proxies


def check_ip(ip, lose_time, waste_time):
    #   命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
    cmd = "ping -n 3 -w 3 %s"
    #   执行命令
    p = sp.Popen(cmd % ip, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    #   获得返回结果并解码
    out = p.stdout.read().decode("gbk")
    #   丢包数
    lose_time = lose_time.findall(out)
    #   当匹配到丢失包信息失败,默认为三次请求全部丢包,丢包数lose赋值为3
    if len(lose_time) == 0:
        lose = 3
    else:
        lose = int(lose_time[0])
    #   如果丢包数目大于2个,则认为连接超时,返回平均耗时1000ms
    if lose > 2:
        #   返回False
        return 1000
    #   如果丢包数目小于等于2个,获取平均耗时的时间
    else:
        #   平均时间
        average = waste_time.findall(out)
        #   当匹配耗时时间信息失败,默认三次请求严重超时,返回平均好使1000ms
        if len(average) == 0:
            return 1000
        else:
            average_time = int(average[0])
            #   返回平均耗时
            return average_time


def initpattern():
    #   匹配丢包数
    lose_time = re.compile(u"丢失 = (\d+)", re.IGNORECASE)
    #   匹配平均时间
    waste_time = re.compile(u"平均 = (\d+)ms", re.IGNORECASE)
    return lose_time, waste_time


def start(proxy):
    # 初始化正则表达式
    lose_time, waste_time = initpattern()
    # 如果平均时间超过200ms重新选取ip
    # 从100个IP中随机选取一个IP作为代理进行访问
    split_proxy1 = proxy.split('://')
    split_proxy2 = split_proxy1[1].split(':')
    # 获取IP
    ip = split_proxy2[0]
    # 检查ip
    average_time = check_ip(ip, lose_time, waste_time)
    if average_time > 200:
        return True
    else:
        return False


def check(proxy):
    if proxy.startswith("https"):
        url = "https://www.baidu.com/js/bdsug.js?v=1.0.3.0"
        proxy_handler = urllib2.ProxyHandler({'https': proxy})
    else:
        url = "http://www.baidu.com/js/bdsug.js?v=1.0.3.0"
        proxy_handler = urllib2.ProxyHandler({'http': proxy})
    opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
    try:
        response = opener.open(url, timeout=3)
        return response.code == 200 and response.url == url
    except Exception:
        return False


def fetch_all(https=False):
    proxies = []
    proxies += fetch_mimvp(https)
    proxies += fetch_xici(https)
    proxies += fetch_66ip(https)
    valid_proxies = []
    for p in proxies:
        if check(p) and start(p):
            valid_proxies.append(p)
    return valid_proxies

