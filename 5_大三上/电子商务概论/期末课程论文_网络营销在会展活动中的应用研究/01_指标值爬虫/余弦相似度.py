#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-12-05 21:53
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : 余弦相似度.py
# @Software: PyCharm

import logging
import re
import warnings

import numpy as np
import jieba

jieba.setLogLevel(logging.INFO)


def get_times(set1, set2, un):  # 定义函数
    times = np.zeros((2, len(un)))  # 创建数组
    j = 0  # 循环变量
    for i in un:  # 循环
        for jj in set1:  # 循环第一个集合
            if jj == i:  # 判断和并集的元素是否相同
                times[0][j] += 1  # 相同则 + 1
        for ii in set2:  # 循环第二个集合
            if ii == i:  # 判断和并集的元素是否相同
                times[1][j] += 1  # 相同则 + 1
        j += 1  # 循环变量自增

    return times  # 返回次数


def similarity(word1, word2):
    a = jieba.lcut(re.sub(r'[].\\/_,$%^&*(+\"\')，|\[（）\s{}【】！@#￥…\s]+', '', word1))
    b = jieba.lcut(re.sub(r'[].\\/_,$%^&*(+\"\')，|\[（）\s{}【】！@#￥…\s]+', '', word2))
    a_set = set(a)
    b_set = set(b)
    un = a_set.union(b_set)
    times = get_times(a, b, un)  # 调用函数
    # print(un)
    # print(times)
    # 计算相似度
    res = np.dot(times[:1][0], times[1:][0]) / (np.linalg.norm(times[:1][0]) * np.linalg.norm(times[1:][0]))
    return res


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    bb = 'CBEE第三届中国厦门全球跨境电商博览会暨中小工厂（出口）展览交易会'
    print(similarity('中国无锡太湖国际机床展览会',
                     '第十四届中国 (无锡) 国际新能源大会暨展览会开'))

