# coding:utf-8
# 采集流程：获取类目url——>获取商品url——>获取产品评价

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


def get_category():
    '''
    从起始页面获取所有类目的url
    :return:
    '''
    start_url = "https://m.helijia.com/?1568276289205#/cats?_k=m3kgjz"  # 河狸家北京站分类页
    page = driver.get_html_brower(start_url)
    categorys = []
    cindex = 0
    for item in browser.find_elements_by_class_name('nav-cell'):
        item.click()
        html = browser.page_source
        doc = pq(html)
        category = dict(
            title=doc.find('li.nav-cell').eq(cindex).text(),
            url=doc.find('a.more').attr('href')
        )
        print(category)
        cindex += 1
        categorys.append(category)
    return categorys


def get_product():
    '''
    从类目列表中（含分页）获取所有产品信息
    :return:
    '''
    categorys = get_category()
    products = []
    for category in categorys:
        browser.get(category['url'])
        page_down()
        html = browser.page_source
        products.append(save_product(html, category))
    return products


def get_review():
    products = r.smembers('helijia_product')
    reviews = []
    if len(products) > 1:
        for product in products:
            product = json.loads(product)
            if check_url(product['url']):
                print(product['url'])
                uid = 'id\=(\w+)'
                pid = re.search(uid, product['url']).group(1)
                review_url = "https://m.helijia.com/comments.html?id=%s&type=product" % pid
                browser.get(review_url)
                html = browser.page_source
                doc = pq(html)
                if doc.find('.no-result-text').size() == 1:
                    delrow = r.srem('helijia_product', json.dumps(product))
                    print('删除url：%s' % product['url'])
                else:
                    page_down(max_time=60)
                    html = browser.page_source
                    reviews.append(save_review(html, product))
                    delrow = r.srem('helijia_product', json.dumps(product))
                    print('删除url：%s' % product['url'])
            else:
                delrow = r.srem('helijia_product', json.dumps(product))
                print('删除url：%s' % product['url'])
    return reviews


def page_down(max_time=300):
    body = browser.find_element_by_tag_name('body')
    t = 0
    while t <= max_time:
        body.send_keys(Keys.END)
        time.sleep(0.2)
        t += 1


def save_product(html, category):
    '''
    从当前页面获取产品列表信息
    :param html: 当前页面html,页面所属类目，页面地址
    :return: 产品列表
    '''
    doc = pq(html)
    items = doc.find('div.content .product-item>.box')
    products = []
    if items.size() > 0:
        for item in items.items():
            product = dict(
                category_title=category['title'],
                category_url=category['url'],
                title=item.find('span.name').text(),
                url=item.find('.product-image-box a').attr('href'),
                img=item.find('.product-image-box .image').attr('src'),
                service_type=item.find('span.service-type').text(),
                price=tools.get_int(item.find('span.round').text()),
                like=tools.get_int(item.find('span.status-text').text()),
                seller=item.find('span.nick-name').text(),
                star=tools.get_star(item.find('img.star').attr('src'))
            )
            r.sadd('helijia_product', json.dumps(product))  # 存储到redis队列
            print(product)
            products.append(product)
    return products


def save_review(html, product):
    doc = pq(html)
    items = doc.find('.comment-item-component')
    reviews = []
    mycol = mydb['helijia_reviews']
    if items.size() > 0:
        for item in items.items():
            review = dict(
                category_title=product['category_title'],
                category_url=product['category_url'],
                product_title=product['title'],
                product_url=product['url'],
                product_seller=product['seller'],
                product_like=product['like'],
                product_price=product['price'],
                product_img=product['img'],
                product_service_type=product['service_type'],
                user=item.find('p.comment-user-mobile').text(),
                user_level=tools.get_str('user_level_(\d)\.png', item.find('.levelImg img').attr('src')),
                comment=item.find('.comment-content').text(),
                star=item.find('.comment-user-star').text(),
                time=item.find('.comment-date').text(),
                comment_img=item.find('.comment-img .image').attr('src'),
            )
            print(review)
            # r.sadd('helijia_reviews', json.dumps(review))  # 存储到redis队列
            mycol.insert_one(review)  # 保存到mongoDB
            reviews.append(review)
    else:
        delrow = r.srem('helijia_product', json.dumps(product))
        print('删除url：%s' % product['url'])
    return reviews


def check_url(url):
    mycol = mydb['helijia_reviews']
    myquery = {"product_url": url}
    mydoc = mycol.count_documents(myquery)
    if mydoc > 0:
        return False
    else:
        return True


def main():
    # get_product()
    get_review()

    browser.close()
