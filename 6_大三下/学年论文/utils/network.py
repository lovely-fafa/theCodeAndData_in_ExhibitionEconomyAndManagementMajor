#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2023-06-02 17:07
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : network.py
# @Software: PyCharm

from typing import Any

import requests
from requests import api


def request(method: str,
            url: str,
            params: dict = None,
            **kwargs) -> str:
    HEADERS = {
        "Connection": "close",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36 ",
        "Referer": "https://you.ctrip.com/"
    }

    cookies = {
        "GUID": "09031018217232548145",
        "nfes_isSupportWebP": "1",
        "_bfaStatusPVSend": "1",
        "MKT_CKID": "1668608048571.ws27n.bxai",
        "_RSG": "x5a3AexNKE4vYuXNa9g4v9",
        "_RDG": "282cd4ea6ffecb2b5e0e38482e0e60469e",
        "_RGUID": "43945fba-0a0e-417b-9e44-a899178788b9",
        "_ga": "GA1.2.1618295057.1683685039",
        "ibulanguage": "CN",
        "ibulocale": "zh_cn",
        "cookiePricesDisplayed": "CNY",
        "MKT_Pagesource": "PC",
        "Session": "smartlinkcode=U130727&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=",
        "Union": "AllianceID=4902&SID=130727&OUID=&createtime=1685693222&Expires=1686298022298",
        "MKT_CKID_LMT": "1685693223573",
        "_RF1": "2409%3A8962%3A5aa%3A1d7a%3Ad51a%3A8a9c%3Ac144%3Acc94",
        "ABTESTTRACE": "EDB82C707F50E98E889B3B9C4C2462987BA2B0238BCF3DEEFA826BF152824D8F0435CCFB0DCD79C3670DE0D1577BE9A0",
        "_bfa": "1.1678373178526.4b2djp.1.1685720827331.1685773971939.25.84.1",
        "_bfs": "1.4",
        "_ubtstatus": "%7B%22vid%22%3A%221678373178526.4b2djp%22%2C%22sid%22%3A25%2C%22pvid%22%3A84%2C%22pid%22%3A0%7D",
        "_bfi": "p1%3D290510%26p2%3D290510%26v1%3D84%26v2%3D83",
        "_bfaStatus": "success",
        "_jzqco": "%7C%7C%7C%7C1685693225727%7C1.1124709360.1678373180699.1685773995920.1685774002712.1685773995920.1685774002712.undefined.0.0.75.75",
        "__zpspc": "9.22.1685773980.1685774002.3%233%7Cwww.bing.com%7C%7C%7C%7C%23"
    }

    resp = api.request(method=method, url=url, params=params, headers=HEADERS, cookies=cookies, **kwargs)
    resp.encoding = 'utf-8'

    return resp.text


if __name__ == '__main__':
    print(request('get', 'https://httpbin.org/ip', proxies={'https': '183.165.250.62:4254'}))
