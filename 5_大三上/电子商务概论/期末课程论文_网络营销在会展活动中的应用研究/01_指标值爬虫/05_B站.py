#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-12-07 10:34
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : B站.py
# @Software: PyCharm

import re
import time
from urllib import parse

import pandas as pd
from tqdm import tqdm
from selenium import webdriver

from 余弦相似度 import similarity

driver = webdriver.Chrome('chromedriver.exe')


def bilibili(name, page):
    if page == 1:
        driver.get(f'https://search.bilibili.com/all?keyword={name}')
    else:
        driver.get(f'https://search.bilibili.com/all?keyword={parse.quote(name)}&page={page}')

    time.sleep(2)
    page_text = driver.page_source
    title_list = re.findall('<div class="(?:to_hide_xs)?(?:video-list-item )?col_3 col_xs_1_5 col_md_2 col_xl_1_7 mb_x40".*?>.*?<h3 class=".*?" title="(.*?)".*?</div>', page_text, re.S)

    return title_list


def get_num(name):
    res = 0
    page = 1
    while True:
        title = bilibili(name=name, page=page)
        if len(title) == 0:
            break
        for one_title in title:
            si = similarity(one_title, name)
            if si >= 0.65:
                res += 1

        page += 1
    return res


if __name__ == '__main__':
    tabel = pd.read_excel('./0_未爬.xlsx')
    check_table = pd.read_excel('./bilibili.xlsx')
    check_list = list(check_table['name'])

    for row in tqdm(range(tabel.shape[0])):
        n = tabel.loc[row, 'name']

        if n not in check_list:
            num = get_num(name=n)
            tabel.loc[row, 'bilibli'] = num
            time.sleep(5)
        else:
            print('over...')

    tabel.to_excel('./bilibili.xlsx', index=None)
