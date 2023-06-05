#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2023-05-30 18:51
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : 整理景点信息到Excel.py
# @Software: PyCharm

import re

import pandas as pd

with open('名单.txt', encoding='utf-8') as f:
    content = f.read()

name = re.sub(r'\[.*?]', '', content, flags=re.S)
info = re.findall(r'\[(.*?)]', content, flags=re.S)
res = []
for i, j in zip(name.split('\n\n'), info):
    res.append([i] + [m.split(',')[0] for m in list(eval(j.replace('\n', '')))])

pd.DataFrame(data=res).to_excel('景点信息.xlsx')
