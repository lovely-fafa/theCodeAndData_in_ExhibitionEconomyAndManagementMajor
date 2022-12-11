#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-12-06 9:56
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : 02_搜狐.py
# @Software: PyCharm


import re
import time

import pandas as pd
from tqdm import tqdm
from selenium import webdriver

from 余弦相似度 import similarity

driver = webdriver.Chrome('chromedriver.exe')


def souhu_news(name):
    driver.get(f'https://search.sohu.com/?keyword={name}')
    time.sleep(5)

    status = True
    js = "return document.documentElement.scrollHeight;"
    height = 0
    while status:
        new_height = driver.execute_script(js)
        # 每执行一次滚动条拖到最后，就进行一次参数校验，并且刷新页面高度
        if new_height > height:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            height = new_height
            time.sleep(1)
        else:
            # 当页面高度不再增加的时候，我们就认为已经是页面最底部，结束条件判断
            # print("滚动条已经处于页面最下方!")
            driver.execute_script('window.scrollTo(0, 0)')  # 把滚动条拖到页面顶部
            break

    time.sleep(2)
    page_text = driver.page_source
    title_noClean_list = re.findall(r'<div class="cards-content-title">(.*?)</div>', page_text, re.S)
    title_list = [re.sub(r'<.*?>', '', i) for i in title_noClean_list]
    return title_list


def get_num(name):
    res = 0
    for one_title in souhu_news(name=name):
        si = similarity(one_title, name)
        # print(si, one_title, name)
        if si >= 0.65:
            res += 1

    return res


if __name__ == '__main__':
    tabel = pd.read_excel('./01_腾讯网.xlsx')
    for row in tqdm(range(tabel.shape[0])):
        num = get_num(name=tabel.loc[row, 'name'])
        tabel.loc[row, '搜狐'] = num
        time.sleep(5)
        # break

    tabel.to_excel('./02_搜狐.xlsx', index=None)


