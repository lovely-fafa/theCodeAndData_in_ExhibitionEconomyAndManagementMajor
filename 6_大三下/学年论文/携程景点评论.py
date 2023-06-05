#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-07-13 10:30
# @Author  : 发发
# @QQ      : 1315337973
# @File    : 携程景点评论.py
# @Software: PyCharm
import csv
import os
import random
import re
from enum import Enum

import pandas as pd
import requests
import math
import time
import fake_useragent
import tqdm
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures
import logging


# x-traceID= r (09031015118730378147-1657677575435-3367604")
# r = t + "-" + (new Date).getTime() + "-" + Math.floor(1e7 * Math.random());
# _fxpcqlniredt: 09031015118730378147 = t = 09031015118730378147  # 定值？


class SortTypeEnum(Enum):
    By_Time = 1
    By_Intelligent = 3


def search_district(search_name):
    """
    根据 行政区 名搜索行政区信息
    :param search_name: 关键词
    :return: ['宁国', '1167', 'http://you.ctrip.com/place/1167.html', '30.63357166', '118.98298102', '1005', '504', '宣城']
    [search, id, url, lat, lon, cityId, districtId, districtName]
    """
    url_search = "https://m.ctrip.com/restapi/h5api/globalsearch/search"
    params = {
        "action": "online",
        "source": "globalonline",
        "keyword": search_name,
        "t": str(time.time()).replace(".", "")[:13]
    }
    resp_search = requests.get(url=url_search, params=params, headers=headers)
    resp_search_text = resp_search.text
    district = re.findall(
        r'\{"id":(.*?),.*?type":"district",.*?"url":"(.*?)","lat":(.*?),"lon":(.*?),"cityId":(.*?),"districtId":(.*?),"districtName":"(.*?)".*?}',
        resp_search_text,
        re.S)
    if len(district) == 0:
        return "noData"
    else:
        district_list = [search_name] + list(district[0])
    return district_list


def get_comment_info_by_id(url):
    """
    根据 景点 id 拿 poiId
    :param scenic_info_turtle:
    :return: [景点 id, poiId, name, point, numOfComment]
    """
    # scenic_info_list = [name] + list(scenic_info_turtle)
    # Id = scenic_info_list[1]
    # url_poiId = f"https://you.ctrip.com/sight/buenosaires931/{Id}.html"
    resp_poiId = requests.get(url=url, headers=headers)
    resp_poiId_text = resp_poiId.text
    poi = re.search(r'"poiId":(.*?),', resp_poiId_text, re.S).group(1)
    return poi


def get_data(poi, page):
    url = "https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList"
    params = {
        "_fxpcqlniredt": "09031015118730378147",
        "x-traceID": f"09031015118730378147-%s-%s" % (str(time.time()).replace(".", "")[:13],
                                                      str(math.floor(10 ** 7 * random.random())))
    }
    js = {
        "arg": {"channelType": 2, "collapseType": 0, "commentTagId": 0, "pageIndex": page, "pageSize": 10, "poiId": poi,
                "sourceType": 1, "sortType": SortTypeEnum.By_Time, "starType": 0},
        "head": {"cid": "09031015118730378147", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888", "syscode": "09",
                 "auth": "", "xsid": "", "extension": []}
    }
    resp_text = requests.post(url=url, params=params, json=js).text
    data_list = re.findall(
        r'"userNick":"(.*?)".*?"score":(.*?),.*?"content":"(.*?)","languageType":"(.*?)".*?"publishTypeTag":"(.*?) 发布',
        resp_text, re.S)
    return data_list


def save_data(data_list, province, search, science):
    # 存文件夹
    if not os.path.exists(r"./data/%s" % province):
        os.mkdir(r"./data/%s" % province)
    if not os.path.exists(r"./data/%s/%s" % (province, search)):
        os.mkdir(r"./data/%s/%s" % (province, search))
    if not os.path.exists(r"./data/%s/%s/%s.csv" % (province, search, science)):
        with open(r"./data/%s/%s/%s.csv" % (province, search, science), mode="a", encoding="utf-8", newline="") as f3:
            dataWriter3 = csv.writer(f3)
            dataWriter3.writerow(col_name)

    f0 = open(r"./data/%s/%s/%s.csv" % (province, search, science), mode="a", encoding="utf-8", newline="")
    dataWriter0 = csv.writer(f0)
    dataWriter0.writerow(data_list)

    # 存文件
    # dataWriter1.writerow(data_list)


def get_scenic(url):
    resp_scenic_text = requests.get(url, headers=headers).text
    # 鄙人不精通 正则表达式，只能出此下策：提取出每一个景点，再提取景点的信息 (因为有些景点是 “暂无点评” 的)
    # 提取景点
    scenic_text_list = re.findall(r'(<a class="guide-main-item" href=".*?" target="_blank">.*?</div></a>)',
                                  resp_scenic_text,
                                  re.S)
    scenic_info_list = []
    for one_scenic in scenic_text_list:
        if "暂无点评" in one_scenic:
            scenic_info_list.append(list(re.findall(
                r'<a class="guide-main-item" href="(.*?)" target="_blank"><.*?<p class="title">(.*?)</p><p class="tag"><span>(.*?)</span>.*/p>',
                one_scenic,
                re.S)[0]).extend("暂无点评"))
        else:
            scenic_info_list.append(list(re.findall(
                r'<a class="guide-main-item" href="(.*?)" target="_blank"><.*?<p class="title">(.*?)</p><p class="tag"><span>(.*?)<!-- -->分</span><span>(.*?)<!-- -->条点评.*?/p>',
                one_scenic,
                re.S)[0]))
    return scenic_info_list


def main(scenic_id):
    """
    主函数呀
    :param name: 搜索的 关键词
    :return: None
    """

    poiId = get_poi_id_by_id(scenic_id)
    # 爬数据啦
    comment_data = get_data(poi=poiId, page=1)




    # for pageNum in tqdm.tqdm(range(1, max_page + 1)):
    #     comment_data = get_data(poi=poiId, page=pageNum)
    #     if len(comment_data) != 0:
    #         for i in comment_data:
    #             save_list = [province] + search_district_list + list(one_scenic_list) + [poiId]
    #             save_list.extend([re.sub(r'(\\u[A-Z\d]{4}|\\n|\s|\n|\t|\\t)', " ", j) for j in i])
    #             save_data(save_list, search=name, science=one_scenic_list[1], province=province)


if __name__ == '__main__':
    logging.basicConfig(filename="logging.log", encoding="utf-8", level=logging.INFO)

    headers = {"Connection": "close"}
    # proxy = {"https": "127.0.0.1"}

    col_name = ["检索词", "检索词id", "检索词url", "lat", "lon", "cityId", "districtId",
                "districtName", "景点url", "景点名", "景点总得分", "评论数", "poiId", "user_name",
                "point", "comment", "language", "date"]

    get_poi_id_by_id()



    # with ThreadPoolExecutor(10) as t:
    #     for one_search in search_data:
    #         try:
    #             t.submit(main, one_search)
    #             logging.info("%s  over", str(one_search))
    #         except Exception as e:
    #             logging.error("\n%s\n%s\n" % (str(e), str(one_search)))
    #             print("\n%s\n%s\n" % (str(e), str(one_search)))



