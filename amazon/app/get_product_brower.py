# coding:utf8
'''
    单线程采集，从redis队列中获取采集地址
'''
from app import db, r
from .models import Category, Product
from .tools import Tools, basedir
from pyquery import PyQuery as pq
import os, json, re, time, threading
from app.brower import Browser
from app.baiduai import BaiDuAI

ai = BaiDuAI()

tools = Tools()
www = 'https://www.amazon.com.au'
driver = Browser()


def main():
    while r.scard('amz_task_url') > 0:
        tools.log('开始启动第%s条采集程序' % str(r.scard('amz_task_url')))
        data = json.loads(r.srandmember('amz_task_url'))
        skus = get_page(data['cid'], data['url'])
        if skus > 0:
            delrow = r.srem('amz_task_url', json.dumps(data))
            if delrow == 1:
                tools.log('采集成功%s条,从队列删除id为%s的任务' % (skus, data['cid']))
        else:
            tools.log('id为%s的任务，采集失败,重试。' % (data['cid']))


def get_page(category_id, category_url, max_page=3):
    '''
    产品采集主
    多线程采集，获取
    :return:返回采集的多页面sku商品数
    '''
    skus = 0
    tools.log('采集页面：%s' % category_url)
    html = driver.get_html_brower(category_url)
    sku = save_product_data(html, category_id)
    # 保存产品数据
    if sku > 0:  # 判断是否抓取成功
        skus += sku
        page = 1
        next_url = next_page(html)
        while next_url:
            # 超出最大页码限制后跳过翻页循环
            page += 1
            if max_page < page:
                tools.log('超出最大页码:%s页限制,跳过翻页循环.' % max_page)
                break

            tools.log('开始采集第%s页商品' % page)
            html2 = driver.get_html_brower(next_url)
            sku2 = save_product_data(html2, category_id)
            if sku2 > 0:  # 判断是否抓取成功
                skus += sku2
                tools.log('第%s页商品采集成功' % page)
                next_url = next_page(html2)
                if next_url:
                    tools.log('下一页是%s' % next_url)
            else:
                return False
    else:
        return False
    return skus


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
            if url is None or url is '':
                return False

        if 'https://www.amazon.com.au' not in url:
            url = www + url

        return url


def save_product_data(html, category_id):
    '''
    # 获取并保存页面的产品数据
    :param html:
    :param category_id:
    :return:返回采集的sku商品数
    '''
    # html = tools.open_file(basedir + '/html/search1.html')
    if html == '' or html is None:
        tools.log('html为空，重试')
        return False

    doc = pq(html)
    items = doc.find('.s-result-item').items()
    sku = 0

    for i in doc.find('h4').items():
        if 'Server Busy' in i.text():
            tools.log('需要输入验证码')
            characters = doc('img').attr('src')  # 验证码图片
            characters = tools.download(characters)
            time.sleep(2)
            if characters:
                captcha = ai.orc_img(imgpath=characters, type='file')  # 识别验证码
                captcha = captcha['words_result'][0]['words']
                tools.log('验证码为：' + captcha)
                input = driver.driver.find_element_by_id('captchacharacters')  # 获取验证码元素
                input.send_keys(captcha)  # 填写验证码表单
                driver.driver.find_element_by_class_name('a-button-text').click()  # 提交验证码

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
                try:
                    commentnum = int(commentnum)
                except Exception as e:
                    commentnum = 0
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
                try:
                    commentnum = int(commentnum)
                except Exception as e:
                    commentnum = 0
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
            sku += 1
        else:
            sku += 1
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
            except Exception as e:
                print('出错位置:save_product')
                tools.log('保存产品：%s 失败' % goods.asin)
                print(e)
                db.rollback()
    return sku


def format_price(str):
    str = str.replace('$', '')
    str = str.replace(',', '')
    reg = '(0|[1-9][0-9]{0,9})(\.\d{1,2})?'
    price = re.search(reg, str)
    if price is not None:
        return price.group()
    else:
        return 0
