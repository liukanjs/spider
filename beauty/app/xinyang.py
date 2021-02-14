# coding:utf-8
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


class XinYangBeauty(object):

    def __init__(self):
        pass

    def get_category(self):
        pass

    def get_hospital(self):
        i = 0
        for start_url in range(395):
            start_url = 'https://y.soyoung.com/hospital/page/%s/' % i
            i += 1
            html = driver.get_html_brower(start_url)

    def save_hospital(self, html):
        doc = pq(html)
        items = doc.find('.filter_list .filter_item')
        if items.size() > 0:
            for item in items.items():
                product = dict(
                    wid=item.attr('data-hosp'),
                    name=item.find('.name').text(),
                    url=item.find('.name a').attr('href'),

                )

    def get_doctor(self):
        pass

    def get_product(self):
        pass

    def get_review(self):
        pass

    def get_diary(self):
        pass

    def get_bbs(self):
        pass


def main():
    xy = XinYangBeauty()
    xy.get_hospital()
