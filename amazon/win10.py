# coding:utf-8
from pyquery import PyQuery as pq
import os, json, re, time, threading
from faker import Factory
import pandas as pd
from app.excel import Excel

fake = Factory().create('zh_CN')
excel = Excel()


def task(keyword, page):
    print('开始采集关键词为"%s"的任务，采集页数%s页' % (keyword, page))
    print(df)


def db(n):
    df = []
    for i in range(n):
        data = dict(
            name=fake.name(),
            phone=fake.phone_number()
        )
        df.append(data)
    df = pd.DataFrame(df)
    return df


if __name__ == '__main__':
    # keyword = input('请输入关键词：')
    # page = input('请输入采集页数：')
    # task(keyword, page)
    # input("程序执行完成，按Enter关闭 <enter>")
    # a = db(3)
    # b = db(5)
    # c = a.append(b)
    # c.to_excel('df.xls')
    # print(c)

    excel.read_to_dict('df.xls')
