#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-12-05 21:50
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : 01_腾讯网.py
# @Software: PyCharm

import re
import time

from faker import Faker
import requests
import pandas as pd
from tqdm import tqdm

from 余弦相似度 import similarity


ua = Faker()
url = ' https://r.inews.qq.com/gw/pc_search/result'

headers = {
    'user-agent': ua.user_agent(),
    'referer': 'https://www.qq.com/',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.qq.com'
}


def tencent_news(search: str, page: int):
    data = {
        'page': page,
        'is_pc': 1,
        'query': search,
        'hippy_custom_version': 10,
        'search_type': 'all',
        'search_count_limit': 10
    }
    resp = requests.post(url, data=data, headers=headers)
    resp_json = resp.json()
    title_list = re.findall(r"'title': '(.*?)',", str(resp_json))
    total_num = resp_json['total_num']

    return title_list, total_num


def get_num(name):
    res = 0
    title, total_num = tencent_news(search=name, page=0)
    for one_title in title:
        si = similarity(one_title, name)
        if si > 0.65:
            res += 1
    max_page = int(total_num / 10) + 1

    if max_page >= 2:
        for page in range(1, max_page):
            title, total_num = tencent_news(search=name, page=page)
            for one_title in title:
                si = similarity(one_title, name)
                if si >= 0.65:
                    res += 1
            time.sleep(1)
        return res

    return res


tabel = pd.read_excel('./0_未爬.xlsx')
for row in tqdm(range(tabel.shape[0])):
    num = get_num(name=tabel.loc[row, 'name'])
    tabel.loc[row, '腾讯网'] = num
    time.sleep(5)

tabel.to_excel('./1_腾讯网.xlsx', index=None)
