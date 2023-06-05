#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2023-05-30 14:49
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : xiecheng.py
# @Software: PyCharm

import logging
import math
import random
import re
import time
from enum import Enum

import pandas as pd
import requests
from tqdm import tqdm

from utils import log, network


class SortTypeEnum(Enum):
    BY_TIME = 1
    BY_INTELLIGENT = 3


class Sight(object):
    COMMENT_COLUMNS = ['nickname', 'point', 'content', 'ip', 'language', 'date']
    BASIC_INFO_COLUMNS = ['name', 'id', 'level', 'comment_count', 'comment_score']

    max_comment_page = None

    def __init__(self, sight_url: str, ip):
        """

        :param sight_url: https://you.ctrip.com/sight/dujiangyan911/4597.html
        """

        self.id = re.search(r'/(\d+)\.html', sight_url).group(1)
        # 应该要做成 ip 池的 但是来不及
        self.proxies = {'https': ip} if ip else None

        # resp_text = requests.get(sight_url, headers=self.HEADERS).text
        resp_text = network.request('get', sight_url, proxies=self.proxies)
        try:
            self.poi_id = re.search(r'"poiId":(\d+),', resp_text).group(1)
        except:
            logging.warning(f'sight_url={sight_url} 没有数据')
            return
        self.poi_name = re.search(r'"poiName":"(.*?)",', resp_text).group(1)
        self.comment_score = re.search(r'"commentScore":(.*?),', resp_text).group(1)
        self.comment_count: int = int(re.search(r'"commentCount":(\d+),', resp_text).group(1))
        level = re.search(r'"poiLevel":(.*?),', resp_text)
        self.poi_level = level.group(1) if level else None
        # self.introduction = re.search(r'"introduction":"(.*?)",', resp_text, re.S).group(1)
        # try:
        # self.policy_info = re.search(r'"policyInfoList":(\[.*?]),', resp_text, re.S).group(1)

    def get_comment_by_page(self, page_num: int, sort_type: SortTypeEnum):

        if not self.max_comment_page:
            max_comment_page = self.set_max_comment_page()
            if page_num > max_comment_page or page_num > 300:
                raise Exception('页码超过最大')

        if page_num > self.max_comment_page or page_num > 300:
            raise Exception('页码超过最大')

        comment_url = "https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList"
        params = {
            "_fxpcqlniredt": "09031018217232548145",
            "x-traceID": f"09031018217232548145-%s-%s" % (str(time.time()).replace(".", "")[:13],
                                                          str(math.floor(10 ** 7 * random.random())))
        }
        js = {
            "arg": {"channelType": 2, "collapseType": 0, "commentTagId": 0, "pageIndex": page_num, "pageSize": 10,
                    "poiId": self.poi_id,
                    "sourceType": 1, "sortType": sort_type.value, "starType": 0},
            "head": {"cid": "09031018217232548145", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                     "syscode": "09",
                     "auth": "", "xsid": "", "extension": []}
        }
        # resp = requests.post(url=comment_url, headers=self.HEADERS, params=params, json=js)
        resp_text = network.request('post', url=comment_url, params=params, json=js, proxies=self.proxies)
        data_list = re.findall(r'"userNick":"(.*?)",.*?"score":(.*?),.*?"content":"(.*?)","languageType":"(.*?)",.*?,"publishTypeTag":"(.*?) 发布.*?,"ipLocatedName":"{0,1}(.*?)"{0,1},',
                               resp_text,
                               re.S)
        res = [list(i) for i in data_list]
        logging.debug(f'proxies={self.proxies} res={res}')
        time.sleep(0.2)
        return res

    def set_max_comment_page(self):
        self.max_comment_page = int(self.comment_count / 10) + 1
        return self.max_comment_page

    def get_comments(self, sort_type: SortTypeEnum, has_progress=True):
        comment = []

        if not self.max_comment_page:
            self.set_max_comment_page()

        actual_max_comment_page = min(self.max_comment_page, 300 + 1)

        if has_progress:
            for page in tqdm(range(1, actual_max_comment_page),
                             total=actual_max_comment_page,
                             postfix=f"{self.poi_name}"):
                one_comment = self.get_comment_by_page(page, sort_type)
                if one_comment:
                    comment.extend(one_comment)
                else:
                    logging.warning(f'{self.poi_name} page={page} 没有数据！')
        else:
            for page in range(1, actual_max_comment_page):
                one_comment = self.get_comment_by_page(page, sort_type)
                if one_comment:
                    comment.extend(one_comment)
                else:
                    logging.warning(f'{self.poi_name} page={page} 没有数据！')

        return comment

    def get_basic_infos(self):
        return [
            self.poi_name,
            self.poi_id,
            self.poi_level,
            self.comment_count,
            self.comment_score,
        ]


if __name__ == '__main__':
    log.config_logging('logger.log')

    url = 'https://you.ctrip.com/sight/longquan2033/45654.html'
    sight = Sight(url, None)

    info = sight.get_basic_infos()
    comments = sight.get_comments(SortTypeEnum.BY_TIME)

    # pd.DataFrame(data=[info + i for i in comments],
    #              columns=sight.BASIC_INFO_COLUMNS + sight.COMMENT_COLUMNS).to_excel(f'{sight.poi_name}.xlsx')
