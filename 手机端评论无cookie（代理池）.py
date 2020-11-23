# -*- coding: utf-8 -*-

import requests
import random
import time
import os
import csv
import sys
import json
from bs4 import BeautifulSoup
import importlib
importlib.reload(sys)


ip_pool = [
        '103.212.92.254',
        '182.253.189.244',
        '190.103.85.37',
        '176.56.107.198',
        '175.42.122.245',
        '123.163.115.126',
        '113.124.93.151',
        '175.42.122.245',
        '49.93.27.56',
        '27.38.154.143',
        '218.250.205.57',
        '121.227.123.244',
        '58.20.230.246',
        '113.59.99.138',
        '125.108.103.169',
        '37.221.204.206'
    ]

ua_pool = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'

    ]



def get_random_ip(ip_pool):
    proxy_list = []
    for ip in ip_pool:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


def get_random_headers(ua_pool):
    ua_list = []
    for ua in ua_pool:
        ua_list.append(ua)
    ua = random.choice(ua_list)
    headers = {
        'method': 'get',
        'Cookie': '请输入你的cookie',
        'Referer': 'https://m.weibo.cn/status/IqtUKo5xH?type=comment',
        'User-Agent': ua,
        'X-Requested-With': 'XMLHttpRequest'
    }
    return headers

def get_page(max_id, id_type):
    params = {
        'max_id': max_id,
        'max_id_type': id_type
    }

    headers = get_random_headers(ua_pool)
    proxies = get_random_ip(ip_pool)
    print(proxies)

    try:
        r = requests.get(url, params=params, headers=headers, proxies=proxies)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('error', e.args)


def parse_page(jsondata):
    if jsondata:
        items = jsondata.get('data')
        item_max_id = {}
        item_max_id['max_id'] = items['max_id']
        #print(item_max_id)
        item_max_id['max_id_type'] = items['max_id_type']
        return item_max_id

def write_csv(jsondata):
    datas = jsondata.get('data').get('data')
    for data in datas:
        created_at = data.get("created_at")
        userid = data.get("user").get("id")
        comment_id_url = data.get('user').get('profile_url')
        like_count = data.get("like_count")
        source = data.get("source")
        floor_number = data.get("floor_number")
        username = data.get("user").get("screen_name")
        comment = data.get("text")
        comment = BeautifulSoup(comment, 'lxml').get_text()
        writer.writerow([username, userid,comment_id_url,created_at, like_count, floor_number, source,
                         json.dumps(comment,  ensure_ascii=False)])

# 要爬取热评的起始url
url = '请输入url'


# 存为csv
path = os.getcwd() + "./292.csv"
csvfile = open(path, 'w',encoding = 'utf-8',newline='')
writer = csv.writer(csvfile)
writer.writerow(['用户名', '用户账号ID','用户主页地址','评论时间', '点赞数', '楼层', '来源', '评论内容'])

maxpage = 请输入爬取页数 #爬取的数量

m_id = 0
id_type = 0
for page in range(0, maxpage):
    print('正在爬取第'+str(page+1)+'页')
    jsondata = get_page(m_id, id_type)
    try:
        write_csv(jsondata)
        results = parse_page(jsondata)
        time.sleep(random.randint(0,1))
        m_id = results['max_id']
        id_type = results['max_id_type']
    except:
        time.sleep(5)
        jsondata = get_page(m_id, id_type)
        try:
            write_csv(jsondata)
            results = parse_page(jsondata)
            time.sleep(random.randint(2,5))
            m_id = results['max_id']
            id_type = results['max_id_type']
        except:
                time.sleep(5)
                jsondata = get_page(m_id, id_type)
                write_csv(jsondata)
                results = parse_page(jsondata)
                time.sleep(random.randint(2,5))
                m_id = results['max_id']
                id_type = results['max_id_type']

