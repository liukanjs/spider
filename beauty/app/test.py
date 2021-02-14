from tools.base import *
from tools.brower import Browser
from queue import Queue
import threading, time, random, json
from pyquery import PyQuery as pq
from selenium import webdriver


def main():
    # dbname = 'helijia_product'
    dbnames = ['daojia58', 'daojia58_reviews']
    for dbname in dbnames:
        mycol = mydb[dbname]
        products = r.smembers(dbname)
        if len(products) > 1:
            for product in products:
                product = json.loads(product)
                x = mycol.insert_one(product)  # 保存到mongoDB
                print(x.inserted_id)


def check_pro():
    products = r.smembers('helijia_product')
    n = 0
    for product in products:
        product = json.loads(product)
        if check_url(product['url']):
            delrow = r.srem('helijia_product', json.dumps(product))
            n += int(delrow)
            print(n)


def check_url(url):
    mycol = mydb['helijia_reviews']
    myquery = {"product_url": url}
    mydoc = mycol.count_documents(myquery)
    if mydoc > 0:
        return True
    else:
        return False


def del_row():
    db = DbTools('helijia_reviews')
    for item in mydb['helijia_reviews'].find():
        query = {'lv2_title': lv2_title}
        update_to_mongo('category', query, category)
        db = DbTools('helijia_reviews')
        query = {'lv2_title': lv2_title}
