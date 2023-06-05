#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2023-05-24 15:41
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : 景点id.py
# @Software: PyCharm

import math
import random
import re
import time
from pprint import pprint

import requests


def search(search_name):
    """
    根据关键词 搜索 相关的旅游景点信息
    :param search_name: 关键词
    :return: [(景点 id, name, point, numOfComment), (景点 id, name, point, numOfComment)]
    """
    url_search = "https://m.ctrip.com/restapi/soa2/20591/getGsOnlineResult"
    params = {
        "_fxpcqlniredt": "09031015118730378147",
        "x-traceID": f"09031015118730378147-%s-%s" % (str(time.time()).replace(".", "")[:13],
                                                      str(math.floor(10 ** 7 * random.random())))
    }
    js = {
        "keyword": search_name, "pageIndex": 0, "pageSize": 12, "tab": "all", "sourceFrom": "", "profile": False,
        "head": {"cid": "09031015118730378147", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888", "syscode": "09",
                 "auth": "", "xsid": "", "extension": []}
    }
    headers = {"Connection": "close"}
    resp_search = requests.post(url=url_search, params=params, headers=headers, json=js)
    resp_search_text = resp_search.text
    scenic_list = re.findall(r'\{"tab":\{.*?"word":"景点","total":.*?},"items":(\[.*?])}', resp_search_text, re.S)  # 景点数据
    if len(scenic_list) == 0:
        return "noData"
    else:
        scenic = scenic_list[0]
    result = re.findall(
        r'"type":"sight","id":(.*?),"code":".*?","word":"(.*?)",.*?"url":"(.*?)".*?commentScore":(.*?),.*?","commentCount":(.*?),.*?}',
        scenic,
        re.S)
    return result


# with open('景点.txt', encoding='utf-8') as f:
#     spots = f.read()
#
# for spot in spots.split('\n'):
#     print(spot)
#     pprint(search(spot))

print(search('天门山国家森林公园'))
