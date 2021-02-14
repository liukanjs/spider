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
tools = Tools()


def get_category():
    '''
    从起始页面获取所有类目的url
    :return:
    '''
    start_url = "https://bj.daojia.com/liren/"  # 北京丽人
    page = driver.get_html_brower(start_url)
    doc = pq(page)
    categorys = []
    for category in doc.find('.main-con ul').eq(0).find('a').items():
        if 'javascript' not in category.attr('href'):
            obj = dict(
                url=category.attr('href'),
                title=category.text(),
            )
            tools.log(obj)
            categorys.append(obj)
    return categorys


def get_product():
    '''
    从类目列表中（含分页）获取所有产品信息
    :return:
    '''
    categorys = get_category()
    products = []
    for category in categorys:
        category_url = category['url']
        category_title = category['title']
        first_page = driver.get_html_brower(category_url)
        products.extend(save_product(first_page, title=category_title, url=category_url))
        next_url = next_page_url(first_page)
        while next_url:
            next_page = driver.get_html_brower(next_url)
            products.extend(save_product(next_page, title=category_title, url=next_url))
            next_url = next_page_url(next_page)
    return products


def get_review():
    products = r.smembers('daojia58')
    reviews = []
    if len(products) > 1:
        for product in products:
            product = json.loads(product)
            if product['sales'] > 1:
                first_page = driver.get_html_brower(product['url'])
                user_btn = driver.driver.find_element_by_class_name('user-btn')
                user_btn.click()
                body = driver.driver.find_element_by_tag_name('body')
                body.send_keys(Keys.END)
                time.sleep(1)
                reviews.extend(save_review(first_page, product=product))
                next_url = next_review_url(html=first_page)
                print(next_url)
                while next_url:
                    next_button = driver.driver.find_element_by_class_name('next-page')
                    next_button.click()
                    body = driver.driver.find_element_by_tag_name('body')
                    body.send_keys(Keys.END)
                    time.sleep(1)
                    next_page = driver.driver.page_source
                    reviews.extend(save_review(next_page, product=product))
                    next_url = next_page_url(next_page)
    return reviews


def next_page_url(html):
    '''
    从当前产品列表页面获取下一页的url
    :param html:当前页面的html
    :return:有则返回url，无则返回False
    '''
    doc = pq(html)
    next_botton = doc.find('li.next-page')
    if next_botton.size() > 0:
        return next_botton.find('a').attr('href')
    else:
        return False


def save_product(html, title, url):
    '''
    从当前页面获取产品列表信息
    :param html: 当前页面html,页面所属类目，页面地址
    :return: 产品列表
    '''
    doc = pq(html)
    items = doc.find('ul.w-search-list.search-list-top li')
    products = []
    if items.size() > 0:
        for item in items.items():
            product = dict(
                category_title=title,
                category_url=url,
                title=item.find('h4.overflow-ellipsis').text(),
                url=item.find('h4.overflow-ellipsis a').attr('href'),
                img=item.find('img.w-search-list-item-img').attr('data-original'),
                service_type=item.find('p.service-type').text(),
                price=tools.get_int(item.find('span.price-num').text()),
                seller=item.find('p.goods-provider').text(),
                sales=tools.get_int(item.find('p.sale-wrapper').text()),
            )
            r.sadd('daojia58', json.dumps(product))  # 存储到redis队列
            print(product)
            products.append(product)
    return products


def save_review(html, product):
    doc = pq(html)
    items = doc.find('.user-list-box ul.user-list-item')
    reviews = []
    if items.size() > 0:
        for item in items.items():
            review = dict(
                category_title=product['category_title'],
                category_url=product['category_url'],
                product_title=product['title'],
                product_url=product['url'],
                product_seller=product['seller'],
                product_sales=product['sales'],
                product_price=product['price'],
                product_img=product['img'],
                product_service_type=product['service_type'],
                user=item.find('li').eq(0).text(),
                comment=item.find('.user-comment').text(),
                star=tools.get_int(item.find('.mask-star').attr('style')) / 100 * 5,
                time=tools.get_time(item.find('.server-time').text()),
                supplement=item.find('.business-supplement').text()
            )
            print(review)
            r.sadd('daojia58_reviews', json.dumps(review))  # 存储到redis队列
            reviews.append(review)
    return reviews


def next_review_url(html):
    doc = pq(html)
    next_botton = doc.find('li.next-page')
    if next_botton.size() > 0:
        return True
    else:
        return False


def main():
    # get_product()
    get_review()

    driver.driver.close()
