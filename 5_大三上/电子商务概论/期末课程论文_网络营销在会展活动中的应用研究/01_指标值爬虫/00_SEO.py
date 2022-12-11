#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-12-06 21:15
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : SEO.py
# @Software: PyCharm

from time import sleep
import re

import pandas as pd
import requests
from tqdm import tqdm


def get_seo_data(domain):
    url = f'https://apistore.aizhan.com/baidurank/siteinfos/7f5925e42b44003c222e899d0cfe0dac?domains={domain}'
    resp_json = str(requests.get(url).json())

    ip = sum([eval(i) for i in re.findall(r"'ip': '(\d+) ~ (\d+)'", resp_json)[0]]) / 2
    br = (eval(re.search(r"'m_br': (\d+)", resp_json).group(1)) +
          eval(re.search(r"'pc_br': (\d+)", resp_json).group(1))) / 2

    return ip, br


if __name__ == '__main__':
    table = pd.read_excel('./0_url.xlsx')
    for row in tqdm(range(table.shape[0])):
        u = table.loc[row, '官网网址']

        if type(u) != float:
            uu = u.split('//')[1].split('/')[0]
            ip, br = get_seo_data(domain=uu)

            table.loc[row, '预计来路'] = ip
            table.loc[row, '百度权重'] = br

            sleep(1)

    table.to_excel('SEO.xlsx', index=None)


