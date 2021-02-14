from app import db
from .models import Category, Product
from .tools import Tools, basedir
from pyquery import PyQuery as pq
import os, json, re

tools = Tools()

www = 'https://www.amazon.com.au'


def once():
    # key = 'tvs'
    # tv2 = 'https://www.amazon.com.au/s?rh=n%3A4851799051%2Cn%3A%214851800051%2Cn%3A4885079051%2Cn%3A4885131051&page=2&qid=1563895106&ref=lp_4885131051_pg_2'
    # html = tools.get_html_brower(tv2)
    # tools.open_file('tvs2.html', html)
    # print('保存')

    html = tools.open_file(basedir + '/html/tvs2.html')
    get_goods_by_category(html, 1)

    '''
    # data = db.query(Category).filter(Category.name.like('tv%'))
    data = db.query(Category).filter(Category.name == 'TVs')
    for i in data:
        item = i.to_dict()
        html = tools.get_html_brower(item['url'])
        tools.save_file('tvs.html', html)
        print('保存')

    catelist = db.query(Category).filter(Category.level == 8)
    print(type(catelist))
    print(type(catelist.first()))
    print(type(catelist.all()))

    for i in catelist:
        print(i.to_dict())

    '''

    '''
    tools.log('开始采集')
    try:
        get_all_lv()
    except Exception as e:
        tools.log('采集出错:$s' % e)
    tools.log('采集完成')
    driver.close()
    
    :return:
    '''


def get_goods_by_category(html, category_id):
    # html = tools.open_file(basedir + '/html/search1.html')
    doc = pq(html)
    items = doc.find('.s-result-item').items()

    for item in items:
        asin = item.attr('data-asin')
        title = item.find('h2').text()
        if asin is None or db.query(Product).filter(Product.asin == asin).count() > 0:
            return False

        is_best_sellers = False
        is_prime = False
        is_amazon = False

        if doc.find('#search').size() == 1:
            # 搜索结果页
            url = item.find('h2>a').attr('href')
            img = item.find('.s-image-square-aspect>img').attr('src')
            seller = ''

            # 价格
            for i in item.find('span.a-color-base').items():
                if '$' in i.text():
                    price = i.text()
                    price = price.replace(' ', '')
                    price = price.replace(',', '')
                    price = price.replace('$', '')

            if item.find('.a-spacing-top-micro>.a-size-small span.a-size-base').size() > 0:
                commentnum = item.find('.a-spacing-top-micro>.a-size-small span.a-size-base').text()
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
                    offersnum = retest.search('\d+', i.text()).group()
                else:
                    offersnum = 0

            # 是否亚马逊自营产品
            if 'amazon' in title or 'amazon' in seller:
                is_amazon = True
        else:
            # 默认类目首页
            seller = item.find('.a-spacing-mini>.a-spacing-none>span.a-size-small.a-color-secondary:last-child').text()
            url = item.find('h2').parent('a').attr('href')
            img = item.find('.a-spacing-base a>img').attr('src')

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
                commentnum = int(item.find('.s-item-container>.a-spacing-none>a').text())
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
                if retest.search('\d+', offersnum) is not None:
                    offersnum = retest.search('\d+', offersnum).group()
                else:
                    offersnum = 0
            else:
                offersnum = 0

            # 价格
            price = item.find('.a-color-price').text().split('-')[0]  # 取第一个价格值
            price = price.replace(' ', '')
            price = price.replace(',', '')
            price = price.replace('$', '')

        goods = dict(
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
            category_id=category_id
        )
        print(goods)




def save_lv(html, url):
    '''
    当浏览到最后一个类目层级时，获取完整的类目资料并存储到数据库
    :return:
    '''

    try:
        doc = pq(html)
        lv = doc.find('#leftNav>ul:first>li').items()
        lv_count = doc.find('#leftNav>ul:first>li').size()
        if lv_count == 0:
            lv = doc.find('#departments>ul:first>li').items()
        a = 1
        cate = Category()
        cate.url = url
        for i in lv:
            if a == 1:
                cate.lv1_name = i.text()
            elif a == 2:
                cate.lv2_name = i.text()
            elif a == 3:
                cate.lv3_name = i.text()
            elif a == 4:
                cate.lv4_name = i.text()
            elif a == 5:
                cate.lv5_name = i.text()
            elif a == 6:
                cate.lv6_name = i.text()
            elif a == 7:
                cate.lv7_name = i.text()
            elif a == 8:
                cate.lv8_name = i.text()
            elif a == 9:
                cate.lv9_name = i.text()

            a += 1
        db.add(cate)
        db.commit()
        print('添加%s级类目成功' % lv_count)
    except Exception as e:
        print(e)


def get_lv3(html):
    try:
        doc = pq(html)
        lv = doc.find('#leftNav>ul>li')
        if lv.size() == 2:
            lv1_name = doc.find('#leftNav .s-ref-indent-neg-micro').eq(0).text()
            lv2_name = doc.find('#leftNav .s-ref-indent-one').eq(0).text()
        elif lv.size() == 1:
            lv1_name = doc.find('#leftNav .s-ref-indent-neg-micro').eq(0).text()

        items = doc.find('#leftNav>ul>ul').eq(0)
        if len(items) > 0:
            for lv3 in items.find('a').items():
                lv3_name = lv3.text()
                url = lv3.attr('href')
                if 'https://www.amazon.com.au' not in url:
                    url = www + url
                cate = Category(
                    lv1_name=lv1_name,
                    lv2_name=lv2_name,
                    lv3_name=lv3_name,
                    url=url
                )
                db.add(cate)
                db.commit()
                print('添加%s成功' % cate.lv3_name)
        else:
            print('未找到三级类目')
    except Exception as e:
        print(e)


def init_cate():
    html = tools.open_file(basedir + '/html/cate.html')

    doc = pq(html)
    items = doc.find('.popover-grouping').items()

    for item in items:
        lv1name = item.find('.popover-category-name').text()
        for lv2 in item.find('.nav_cat_links>li>a').items():
            lv2name = lv2.text()
            url = lv2.attr('href')
            url_count = db.query(Category).filter(Category.url == url).count()
            if 'All' in lv2name and url_count == 0 and '/b/' in url:
                lv2name = lv2name.replace('All ', '')
                if 'https://www.amazon.com.au' not in url:
                    url = www + url
                cate = Category(
                    lv1_name=lv1name,
                    lv2_name=lv2name,
                    url=url
                )
                db.add(cate)
                db.commit()
                print('添加%s成功' % cate.lv2_name)


'''

    # site = 'https://www.amazon.com.au/gp/site-directory?ref_=nav_shopall_btn'
    # html = tools.get_html(url=site)
    # tools.save_file(filename='cate.html', content=html)
    
'''


def get_all_html():
    '''
    file_list = os.listdir(basedir + '/html/')
    for file in file_list:
        print('开始读取' + file)
        html = tools.open_file(basedir + '/html/' + file)
        get_lv3(html)

    items = db.query(Category).all()
    for item in items:
        url = item.to_dict()['url']
        lv2name = item.to_dict()['lv2_name']
        if 'https://www.amazon.com.au/b/' in url:
            html = tools.get_html_brower(url=url)
            tools.save_file(lv2name + '.html', html)
            print('采集保存页面:%s' % lv2name)

    driver.close()
    '''

    # html = tools.get_html_brower(www)
    # tools.save_file('index.html', html)
