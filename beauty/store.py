# -*- coding: utf-8 -*-
# @Time    : 2020/6/1 17:01
# @Author  : Ken
# @Email   : 54191225@qq.com
# @File    : store.py
# @Remarks :

import requests,datetime
import pandas as pd

headers = {
    'Host': 'zxym.live',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '145',
    'Origin': 'https://zxym.live',
    'Connection': 'keep-alive',
    'Referer': 'https://zxym.live/Mall/OrderConsignment/OrderConsignmentList?title=%E4%BB%A3%E9%94%80%E8%AE%A2%E5%8D%95&_t=419303&_winid=w9657',
    'Cookie': '.AspNetCore.Cookies=CfDJ8N8lxc0IVqxCvpnk3ChCO4VU9WyxhU-CYFen_SXBPSRdh_rJqsS-M7DW8iq-tTqLPZrxeTdki211RXlmBpRaHloXMydzVy0cPS3fhuNTXO0rU7LTGUzL3Jz4o4S_tvV9q6nfh1gZAxVvgUIfFpDs5fRuP3zAy6B4jYtORnGwV8n9TPcvLPkKQuqXpM9J3g7Dy55BH6-C6T4Aw4Gux4vPQv3X5wuuJUsMbl57QJ09iVA7pQ2Zc-KLgFqa6CQevckjJc06PHP4EgVZ4iPUbViX-u_vH7UCj7ZKYQTmGKyGBzNLh4n-xsGontNbiIiZPP4jpZFmxsulJ9udyh_z4rGwzgMUimBYibxjnQrXnRl1FZHPa72zy3s8dAdthJwz7b4yiw7bbL2GOO7TnGeYBG5LbCbo9kMRNSd3ODF6E94Fe9CXl1yJGkIyqPKjI01DBfapmQ',
    'TE': 'Trailers'
}

if __name__ == '__main__':
    arr = []
    for i in range(2):
        start = datetime.datetime.now()
        pyloady = dict(
            filterCondition='',
            OtherFlag='',
            IsLazyLoad='false',
            pageIndex=i,
            pageSize=100,
            sortField='',
            sortOrder=''
        )

        url = 'https://zxym.live/Mall/GoodsFeatures/FetchPaged'
        r = requests.post(url, headers=headers, data=pyloady)
        result = r.json().get('data')
        arr.extend(result)
        end = datetime.datetime.now()
        print(f'第{i}条，耗时：{(end-start).seconds}秒')
    dataframe = pd.DataFrame(arr)
    dataframe.to_excel('优品券商品.xlsx')
