#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2023-06-01 21:45
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : 森林公园爬虫.py
# @Software: PyCharm

import logging
from concurrent import futures

import pandas as pd
from tqdm import tqdm

from utils import log
from xiecheng import Sight, SortTypeEnum


def main(sight_url, ip):
    logging.info(f'sight_url={sight_url} ip={ip}')
    try:
        sight = Sight(sight_url, ip)
        comments = sight.get_comments(SortTypeEnum.BY_TIME, True)
        infos = sight.get_basic_infos()
        logging.info(f'sight_url={sight_url} ip={ip} infos={infos}')
        result.extend([infos + i for i in comments])
    except Exception as e:
        logging.error(f'sight_url={sight_url} ip={ip} | {e}')


if __name__ == '__main__':

    urls = ['https://you.ctrip.com/sight/1/107700.html',
            'https://you.ctrip.com/sight/1/5295.html',
            'https://you.ctrip.com/sight/2584/109983.html',
            'https://you.ctrip.com/sight/639/74756.html',
            'https://you.ctrip.com/sight/120084/52423.html',
            'https://you.ctrip.com/sight/1446026/17768.html',
            'https://you.ctrip.com/sight/2138/63243.html',
            'https://you.ctrip.com/sight/216/10565.html',
            'https://you.ctrip.com/sight/2464/1412350.html',
            'https://you.ctrip.com/sight/2044571/17466.html',
            'https://you.ctrip.com/sight/2/5956.html',
            'https://you.ctrip.com/sight/492/1833139.html',
            'https://you.ctrip.com/sight/688/49155.html',
            'https://you.ctrip.com/sight/164/8797.html',
            'https://you.ctrip.com/sight/622/56407.html',
            'https://you.ctrip.com/sight/23/56867.html',
            'https://you.ctrip.com/sight/2861/16640.html',
            'https://you.ctrip.com/sight/2852/140900.html',
            'https://you.ctrip.com/sight/2937/14850.html',
            'https://you.ctrip.com/sight/152/6773.html',
            'https://you.ctrip.com/sight/152/136185.html',
            'https://you.ctrip.com/sight/707/22156.html',
            'https://you.ctrip.com/sight/981/3233.html',
            'https://you.ctrip.com/sight/158/10340.html',
            'https://you.ctrip.com/sight/158/112754.html',
            'https://you.ctrip.com/sight/2059/76648.html',
            'https://you.ctrip.com/sight/2154/128450.html',
            'https://you.ctrip.com/sight/2776/52661.html',
            'https://you.ctrip.com/sight/486/54314.html',
            'https://you.ctrip.com/sight/1446320/11723.html',
            'https://you.ctrip.com/sight/2637/65268.html',
            'https://you.ctrip.com/sight/23/8360.html']

    ips = ''''''.split('\n') * 2  # ip 池

    log.config_logging('logger.log')

    result = []

    tasks = []
    with futures.ThreadPoolExecutor(15) as t:
        for url, ip in zip(urls, ips):
            tasks.append(t.submit(main, url, ip.strip()))

        for task in tqdm(futures.as_completed(tasks), total=len(tasks)):
            task.result()

    # pd.DataFrame(result).to_excel('景点评论.xlsx')
