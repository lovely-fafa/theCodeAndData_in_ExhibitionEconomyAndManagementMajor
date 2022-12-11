#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-12-04 19:39
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : 中国会展网.py
# @Software: PyCharm

# https://www.cnexpo.com/
# https://www.cnexpo.com/zhanhui/starttime/20220101/endtime/20221231.html?type=0&category_id=0&city_id=0&order=2&sort=0&over=0&page=1

import csv
import re

import requests
from tqdm import tqdm


def get_more_info(arg: tuple):
    url_item = f'https://www.cnexpo.com{arg[0]}'
    res_list = list(arg)
    res_list[0] = url_item
    resp_item = requests.get(url_item)
    resp_item_text = resp_item.text

    place = re.search(r'<i class="iconfont icon-dingwei"></i><span>(.*?)</span></p>', resp_item_text, re.S).group(1)
    area = re.search(r'<span>展览面积</span>.*?<em>(.*?)</em>.*?<b>平方米</b>',
                     resp_item_text,
                     re.S).group(1).replace(',', '')
    attend_num = re.search(r'<span>参展商数量</span>.*?<em>(.*?)</em>.*?<b>家</b>',
                           resp_item_text,
                           re.S).group(1).replace(',', '')
    professionalVisitors_num = re.search(r'<span>专业观众数量</span>.*?<em>(.*?)</em>.*?<b>人</b>',
                                         resp_item_text,
                                         re.S).group(1).replace(',', '')
    res_list.extend([place, area, attend_num, professionalVisitors_num])
    res_list = [j.strip() for j in res_list]

    if '<span class="t_red">(延期会展)</span>' in resp_item_text:
        res_list.append('是')
    else:
        res_list.append('否')

    return res_list


all_data = []
for page in tqdm(range(1, 12)):
    url = f'https://www.cnexpo.com/zhanhui/starttime/20220101/endtime/20221231.html?' \
          f'type=0&category_id=0&city_id=0&order=2&sort=0&over=0&page={page}'
    resp = requests.get(url=url)
    index_regex_obj = re.compile(r'<p class="text-overflow"><a href="(.*?)" target="_blank".*?title="(.*?)">.*?<a '
                                 r'href=".*?" class="t_red" target="_blank">\[(.*?)]</a>.*?</i>时间：('
                                 r'\d\d\d\d-\d\d-\d\d) ~ (.*?)</p>.*?</i>地点：(.*?)</p>',
                                 re.S)
    for i in index_regex_obj.findall(resp.text):
        res = get_more_info(i)
        all_data.append(res)


with open('all_data.csv', mode='w', encoding='utf-8', newline='') as f:
    dataWriter = csv.writer(f)
    dataWriter.writerow(['url', 'name', 'type', 'star', 'end', 'province', 'place',
                         'area', 'attend_num', 'professionalVisitors_num', 'postpone'])
    dataWriter.writerows(all_data)
