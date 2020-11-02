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

# 要爬取热评的起始url
url = 'https://m.weibo.cn/comments/hotflow?id=4514929162294606&mid=4514929162294606&max_id_type=0'
headers = {
    'method':'get',
    'Cookie': 'WEIBOCN_FROM=1110006030; loginScene=102003; SUB=_2A25ymJiRDeRhGeNM71oS8ifKzz6IHXVuYjjZrDV6PUJbkdAKLWzEkW1NTgP5MDyho1vEiVgSERSFMi08PwJwfdtG; SUHB=0vJITUIBWWEkoX; _T_WM=24461897718; XSRF-TOKEN=7f2b2d; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4484282368568436%26luicode%3D20000061%26lfid%3D4484282368568436%26uicode%3D20000061%26fid%3D4484282368568436',
    'Referer': 'https://m.weibo.cn/status/IznwCgpTc?filter=hot&root_comment_id=0&type=comment',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_page(max_id, id_type):
    params = {
        'max_id': max_id,
        'max_id_type': id_type
    }
    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('error', e.args)


def parse_page(jsondata):
    if jsondata:
        items = jsondata.get('data')
        item_max_id = {}
        item_max_id['max_id'] = items['max_id']
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

# 存为csv
path = os.getcwd() + "/#李文亮妻子在武汉生下男婴#.csv"
csvfile = open(path, 'w',encoding = 'utf-8')
writer = csv.writer(csvfile)
writer.writerow(['用户名', '用户账号ID','用户主页地址','评论时间', '点赞数', '楼层', '来源', '评论内容'])

maxpage = 12 #爬取的数量
m_id = 0
id_type = 0
for page in range(0, maxpage):
    print('正在爬取第'+str(page+1)+'页')
    jsondata = get_page(m_id, id_type)
    write_csv(jsondata)
    results = parse_page(jsondata)
    time.sleep(random.randint(1,4))
    m_id = results['max_id']
    id_type = results['max_id_type']
