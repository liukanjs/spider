# coding:utf8
'''
多线程采集
'''

from app import db
from .models import Category, Product
from .tools import Tools, basedir
from pyquery import PyQuery as pq
import os, json, re, time, threading
from queue import Queue

tools = Tools()
www = 'https://www.amazon.com.au'
q = Queue()


def main():
    tools.log('开始启动采集程序')
    # items = db.query(Category).filter(Category.level > 7)

    # 筛选类目数据获得类目列表，从而开始爬取数据
    keys = ['Skin Care Tools', 'dogs']
    for key in keys:
        items = db.query(Category).filter(Category.name.like('%' + key + '%'))

        tools.log('采集类目%s条' % items.count())
        for i in items:
            category_url = i.to_dict()['url']
            category_id = i.to_dict()['id']
            data = {
                'url': category_url,
                'id': category_id,
            }
            q.put(data)
            # get_page(category_id, category_url)

        count = items.count()

        th1 = threading.Thread(target=th_get_page, args=(count,))
        # th2 = threading.Thread(target=th_get_page, args=(int(count / 4),))
        # th3 = threading.Thread(target=th_get_page, args=(int(count / 4),))
        # th4 = threading.Thread(target=th_get_page, args=(int(count / 4),))

        th1.start()
        # th2.start()
        # th3.start()
        # th4.start()

        th1.join()
        # th2.join()
        # th3.join()
        # th4.join()


def get_data_by_req():
    # 单线程采集
    tools.log('开始启动采集程序')
    items = db.query(Category).filter(Category.level > 7)
    tools.log('采集类目%s条' % items.count())
    for i in items:
        category_url = i.to_dict()['url']
        category_id = i.to_dict()['id']
        data = {
            'url': category_url,
            'id': category_id,
        }
        get_page(category_id, category_url)


def th_get_page(num):
    for i in range(num):
        data = q.get()
        get_page(data['id'], data['url'])
        time.sleep(2)
        print(str(threading.current_thread()) + ' %s采集页面:%s' % (data['id'], data['url']))


def get_page(category_id, category_url):
    '''
    产品采集主
    多线程采集，获取
    :return:
    '''
    tools.log(str(threading.current_thread()) + '采集页面：%s' % category_url)
    html = tools.get_html_req(category_url)
    # 保存产品数据
    save_product_data(html, category_id)
    tools.log(str(threading.current_thread()) + '第1页商品采集成功')

    page = 1
    next_url = next_page(html)
    print('next page:' + str(next_url))
    while next_url:
        page += 1
        tools.log(str(threading.current_thread()) + '开始采集第%s页商品' % page)
        html2 = tools.get_html_req(next_url)
        save_product_data(html2, category_id)
        tools.log(str(threading.current_thread()) + '第%s页商品采集成功' % page)
        next_url = next_page(html2)
        if next_url:
            tools.log('下一页是%s' % next_url)


def next_page(html):
    '''
    从当前页面获取下一页的url，否则返回false
    :param html:
    :return:
    '''

    doc = pq(html)
    if doc.find('.a-disabled.a-last').size() == 1:
        return False
    else:
        if doc.find('#pagnNextLink').size() > 0:
            # 类目页
            url = doc.find('#pagnNextLink').attr('href')
        else:
            # 搜索结果页
            url = doc.find('.a-last>a').attr('href')

        if 'https://www.amazon.com.au' not in url:
            url = www + url

        print(str(threading.current_thread()) + '下一页：' + url)
        return url


def get_category_by_key(key=None):
    '''
        # 通过关键词或类目关键词模糊查找类目信息
        # 无关键词，则搜索所有3三级以上类目
    :param key:
    :return:
    '''
    category = []
    if key is not None:
        sql = db.query(Category).filter(Category.name.like('%' + key + '%'))
        for i in sql:
            item = i.to_dict()
            if item['level'] >= 3:  # 仅抓取三级以上类目商品
                category.append(item)
    else:
        sql = db.query(Category).filter(Category.level >= 3)
        for i in sql:
            item = i.to_dict()
            if item['level'] >= 3:  # 仅抓取三级以上类目商品
                category.append(item)
    return category


def save_product_data(html, category_id):
    '''
    # 获取并保存页面的产品数据
    :param html:
    :param category_id:
    :return:
    '''
    # html = tools.open_file(basedir + '/html/search1.html')
    doc = pq(html)
    items = doc.find('.s-result-item').items()

    for item in items:
        asin = item.attr('data-asin')
        title = item.find('h2').text()

        is_best_sellers = False
        is_prime = False
        is_amazon = False
        offersnum = 0
        price = 0

        if doc.find('#search').size() == 1:
            # 搜索结果页
            url = item.find('h2>a').attr('href')
            img = item.find('.s-image-square-aspect>img').attr('src')
            if img is None:
                for i in item.find('img[class*="image"]').items():
                    img = i.attr('src')

            if url is None:
                continue
            if 'https://www.amazon.com.au' not in url:
                url = www + url
            seller = ''

            # 价格
            for i in item.find('span.a-color-base').items():
                if '$' in i.text():
                    price = i.text()
                    price = format_price(price)
            if price == 0:
                price = item.find('.a-offscreen').text()
                price = format_price(price)

            if item.find('.a-spacing-top-micro>.a-size-small span.a-size-base').size() > 0:
                commentnum = item.find('.a-spacing-top-micro>.a-size-small span.a-size-base').text()
                commentnum = commentnum.replace(',', '')
            else:
                commentnum = 0

            # 评分
            if item.find('.a-icon-alt').size() > 0:
                star = item.find('.a-icon-alt').text().split(' ')[0]
            else:
                star = 0

            # 跟卖数offers
            for i in item.find('a.a-link-normal').items():
                if 'offer' in i.text():
                    offersnum = re.search('\d+', i.text()).group()

            # 是否亚马逊自营产品
            if 'amazon' in title or 'amazon' in seller:
                is_amazon = True
        else:
            # 默认类目首页
            seller = item.find('.a-spacing-mini>.a-spacing-none>span.a-size-small.a-color-secondary:last-child').text()
            url = item.find('h2').parent('a').attr('href')
            if url is None:
                continue
            if 'https://www.amazon.com.au' not in url:
                url = www + url

            img = item.find('.a-spacing-base a>img').attr('src')
            if img is None:
                for i in item.find('img[class*="image"]').items():
                    img = i.attr('src')

            # 是否为Best Seller
            if item.find('.a-badge-label').size() > 0:
                is_best_sellers = True
            # 是否支持prime
            if item.find('.a-icon-prime').size() > 0:
                is_prime = True
            # 是否亚马逊自营产品
            if 'amazon' in title or 'amazon' in seller:
                is_amazon = True
            # 评价数
            if item.find('.s-item-container>.a-spacing-none>a').size() > 0:
                commentnum = item.find('.s-item-container>.a-spacing-none>a').text()
                commentnum = commentnum.replace(',', '')

            else:
                commentnum = 0

            # 评分
            if item.find('.a-icon-alt').size() > 0:
                star = item.find('.a-icon-alt').text().split(' ')[0]
            else:
                star = 0

            # 跟卖数offers
            if item.find('a>span.a-color-secondary').size() > 0:
                offersnum = item.find('a>.a-color-secondary').text()
                if re.search('\d+', offersnum) is not None:
                    offersnum = re.search('\d+', offersnum).group()
                else:
                    offersnum = 0
            else:
                offersnum = 0

            # 价格
            price = item.find('.a-color-price').text().split('-')[0]  # 取第一个价格值
            price = format_price(price)

        if asin is None or db.query(Product).filter(Product.asin == asin).count() > 0:
            tools.log('商品:%s，已采集，跳过' % asin)
        else:
            goods = Product(
                title=title,
                url=url,
                seller=seller,
                img=img,
                asin=asin,
                price=float(price),
                commentnum=int(commentnum),
                star=float(star),
                offersnum=int(offersnum),
                is_prime=is_prime,
                is_amazon=is_amazon,
                is_best_sellers=is_best_sellers,
                category_id=category_id,
            )
            try:
                db.add(goods)
                db.commit()
                tools.log('保存产品：%s 成功' % goods.asin)
                time.sleep(0.2)
            except Exception as e:
                tools.log('保存产品：%s 失败' % goods.asin)
                print(e)
                db.rollback()


def format_price(str):
    str = str.replace('$', '')
    str = str.replace(',', '')
    reg = '(0|[1-9][0-9]{0,9})(\.\d{1,2})?'
    price = re.search(reg, str)
    if price is not None:
        return price.group()
    else:
        return 0
