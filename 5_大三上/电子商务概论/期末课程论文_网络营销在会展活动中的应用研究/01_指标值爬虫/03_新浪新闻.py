#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-12-06 11:21
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : 03_新浪新闻.py
# @Software: PyCharm
import re
import time

import pandas as pd
import requests
from tqdm import tqdm

from 余弦相似度 import similarity


def xinlang_news(name, page):
    url = 'https://search.sina.com.cn/news'
    data = {
        'q': name,
        'c': 'news',
        'range': 'all',
        'size': 10,
        'page': page,
    }
    resp_text = requests.post(url, data=data).text
    title_noClean_list = re.findall(r'<h2><a href=".*?" target="_blank">(.*?)</h2>',
                                    resp_text,
                                    re.S)
    title_list = [re.sub(r'<.*?>', '', i.strip()) for i in title_noClean_list]
    return title_list


def get_num(name):
    res = 0
    page = 1
    while True:
        title = xinlang_news(name=name, page=page)
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


tabel = pd.read_excel('./02_搜狐.xlsx')
for row in tqdm(range(tabel.shape[0])):
    num = get_num(name=tabel.loc[row, 'name'])
    tabel.loc[row, '新浪新闻'] = num
    time.sleep(5)

tabel.to_excel('./03_新浪新闻.xlsx', index=None)
