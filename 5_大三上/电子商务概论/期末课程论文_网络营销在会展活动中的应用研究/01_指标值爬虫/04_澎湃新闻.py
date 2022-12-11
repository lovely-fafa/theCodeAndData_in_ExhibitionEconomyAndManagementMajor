#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-12-06 11:40
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : 04_澎湃新闻.py
# @Software: PyCharm

import re
import time

import pandas as pd
import requests
from faker import Faker
from tqdm import tqdm

from 余弦相似度 import similarity

ua = Faker()
url = ' https://r.inews.qq.com/gw/pc_search/result'

headers = {
    'user-agent': ua.user_agent(),
    'Referer': 'https://www.thepaper.cn/',
    'Cookie': 'Hm_lvt_94a1e06bbce219d29285cee2e37d1d26=1670297708; acw_tc=76b20f6316702977082552791e12a46a3881fa5f801feea05cbc01b21f3a23; ariaDefaultTheme=undefined; Hm_lpvt_94a1e06bbce219d29285cee2e37d1d26=1670297720'
}


def pengpai_news(name, page):
    url = 'https://api.thepaper.cn/contentapi/cont/search/news'
    data = {'k': name, 'orderType': 3, 'pageNum': page, 'pageSize': 10, 'searchType': 1}
    resp_json = requests.post(url, json=data, headers=headers).json()
    title_noClean_list = []
    for i in resp_json['data']['list']:
        title_noClean_list.append(i['name'])
    title_list = [re.sub(r'<.*?>', '', i) for i in title_noClean_list]
    return title_list


def get_num(name):
    res = 0
    page = 1
    while True:
        title = pengpai_news(name=name, page=page)
        if len(title) == 0:
            break
        for one_title in title:
            si = similarity(one_title, name)
            print(si, one_title, name)
            if si >= 0.65:
                res += 1

        page += 1
        time.sleep(1)
    return res


tabel = pd.read_excel('./03_新浪新闻.xlsx')
for row in tqdm(range(tabel.shape[0])):
    num = get_num(name=tabel.loc[row, 'name'])
    tabel.loc[row, '澎湃新闻'] = num
    time.sleep(5)

tabel.to_excel('./04_澎湃新闻.xlsx', index=None)
