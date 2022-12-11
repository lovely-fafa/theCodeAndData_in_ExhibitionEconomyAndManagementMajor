#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-12-07 11:45
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : 展会.py
# @Software: PyCharm
import time
from urllib import parse

import pandas as pd
import requests
from faker import Faker
from tqdm import tqdm

ua = Faker()
headers = {
    'user-agent': ua.user_agent(),
}


def quzhanwang(name):
    url = f'https://www.qufair.com/convention/search_key/?key={parse.quote(name)}'
    resp = requests.get(url=url, headers=headers)

    if '抱歉，未搜索到' in resp.text:
        return 0
    else:
        return 1


def juzhanwang(name):
    name = name.split(' ')[0]
    url = f'https://www.jufair.com/exhibition/?keyword={parse.quote(name)}'
    resp = requests.get(url=url, headers=headers)
    with open('0.html', encoding='utf-8', mode='w') as f:
        f.write(resp.text)

    if '非常抱歉，没有搜索到相关展会信息！' in resp.text:
        return 0
    else:
        return 1


tabel = pd.read_excel('./0_未爬.xlsx')
for row in tqdm(range(tabel.shape[0])):
    n = tabel.loc[row, 'name']

    tabel.loc[row, '去展网'] = quzhanwang(name=n)
    tabel.loc[row, '聚展'] = juzhanwang(name=n)
    time.sleep(5)

tabel.to_excel('./会展网站.xlsx', index=None)
