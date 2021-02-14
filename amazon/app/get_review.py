# coding:utf-8
# 采集商品评价信息

from app import db
from .models import Product
from .tools import Tools, basedir
from pyquery import PyQuery as pq
import os, json, re, time, threading, redis

tools = Tools()

site = 'https://www.amazon.com.au/Fashion-21-alloy-Rose-Style/dp/B07TL2PR76/ref=sr_1_80?qid=1565695548&s=apparel&sr=1-80'
html = tools.get_html_req(url=site)
tools.save_file(filename='sku.html', content=html)
