# -*- coding: utf-8 -*-
# @Time    : 2019/12/8 23:47
# @Author  : Ken
# @Email   : 54191225@qq.com
# @File    : map.py
# @Remarks : 腾讯地图



from tools.base import *
from tools.tools import Tools
from tools.brower import Browser
from queue import Queue
import threading, time, random, json, re
from pyquery import PyQuery as pq
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = Browser()
browser = driver.driver
tools = Tools()



def start():
    '''
    从起始页面获取所有类目的url
    :return:
    '''
    start_url = "https://map.qq.com/"  # 河狸家北京站分类页
    page = driver.get_html_brower(start_url)

