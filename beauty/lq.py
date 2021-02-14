# -*- coding: utf-8 -*-
# @Time    : 2020/6/1 16:16
# @Author  : Ken
# @Email   : 54191225@qq.com
# @File    : lq.py
# @Remarks :

import requests, datetime,click
import pandas as pd
import pymongo

myclient = pymongo.MongoClient("mongodb://120.24.39.11:32017/")
mydb = myclient["lq"]
mycol = mydb["order"]

headers = {
    'Host': 'zxym.live',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '144',
    'Origin': 'https://zxym.live',
    'Connection': 'keep-alive',
    'Referer': 'https://zxym.live/Mall/OrderConsignment/OrderConsignmentList?title=%E4%BB%A3%E9%94%80%E8%AE%A2%E5%8D%95&_t=543200&_winid=w731',
    'Cookie': '.AspNetCore.Cookies=CfDJ8Jpo6YIFxrBFgFp9f4vTRdwF1sKz6Se2TmujAju53xGwg75jv61EVtGBkb0DYtbkzyL3-DKj_6vxZFZf2p4PL2lf4TCih4iHOfRDuWN3Ih5Vf0ltNVsfRTLcHy-_hZRNaPwmZme8uYp4z92qDEDP-D5j7UUOPvAzc1NRH9w3pB6vn87kS6Eo3WUVlNJBJmP-3sditAMqm513Myxupj5YdOH6V7nTZzCixwXLUQCdsHUAR0Oi6p6J8eKYWtiCEhnuQD4_sRIw_K-R9T7-HmCurf21dSOvgCVgfQ1zOYocvQae7NFK4d7XYF5L3KxRsHOfvtXaoqRuRSZRNWusHn7m8B7HYJvW9W2J30zt2ypif0hS3Fo4plLR9anDAT6nzwbB5YDlKLj2neM8MF-bXCUotZVHuu-4SwGHrdKPplV6m6c5VVO13IpAdqxN1EVhRbwpAw',
    'TE': 'Trailers'
}


def getData(page):
    start = datetime.datetime.now()
    pyloady = dict(
        OtherFlag='',
        IsLazyLoad='false',
        pageIndex=page,
        pageSize=100,
        sortField='DDefine1',
        sortOrder='asc'
    )

    url = 'https://zxym.live/Mall/OrderConsignment/FetchPaged'
    r = requests.post(url, headers=headers, data=pyloady)
    result = r.json().get('data')
    end = datetime.datetime.now()
    print(f'第{i}条，耗时：{(end - start).seconds}')
    return result


if __name__ == '__main__':
    for i in range(1763,2618):
        try:
            x = mycol.insert_many(getData(i))
            # 输出插入的所有文档对应的 _id 值
            # print(x.inserted_ids)
        except Exception as e:
            print(e)
            pass
