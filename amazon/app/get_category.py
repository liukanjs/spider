from app import db, driver
from .models import Category, Product
from .tools import Tools, basedir
from pyquery import PyQuery as pq
import os, json, re

tools = Tools()
www = 'https://www.amazon.com.au'


def get_all_lv():
    '''
    1.通过一级类目ID得到所有一级类目的url
    2.通过三级类目url得到所有二级类目的url
    3.通过三级类目url得到所有四级类目的url，如果没有就终止循环，进行下一个
    4.通过四级类目url得到五级类目的url，如果没有就终止循环，进行下一个
    5....
    6.将所有最底层类目的url存储到数据库
    :return:
    '''

    # 1.获取第一层
    cate_id = tools.open_file(basedir + '/log/lv1.json')
    lv1_ids = json.loads(cate_id, encoding='utf-8')
    for i in lv1_ids['browseElements']:
        amz_id = i['id']
        name = i['label']
        url = 'https://www.amazon.com.au/b?ie=UTF8&node=%s' % amz_id
        cate1 = Category(
            name=name,
            url=url,
            amz_id=amz_id,
            level=1
        )
        db.add(cate1)
        db.commit()
        tools.log('添加1级类目%s成功' % cate1.name)

        # 获取第二层类目
        lv2_html = tools.get_html_brower(cate1.url)
        lv2_data = get_lv(lv2_html)
        for lv2 in lv2_data:
            cate2 = Category(
                name=lv2['name'],
                url=lv2['url'],
                level=2,
                top_id=cate1.id,
                amz_id = re.search('3A(\d+)&', lv2['url']).group(1)
            )
            db.add(cate2)
            db.commit()
            tools.log('添加2级类目%s成功' % cate2.name)

            # 获取第三层类目
            lv3_html = tools.get_html_brower(cate2.url)
            lv3_data = get_lv(lv3_html)
            if len(lv3_data) > 0:
                for lv3 in lv3_data:
                    cate3 = Category(
                        name=lv3['name'],
                        url=lv3['url'],
                        level=3,
                        top_id=cate2.id,
                        amz_id = re.search('3A(\d+)&', lv3['url']).group(1)
                    )
                    db.add(cate3)
                    db.commit()
                    tools.log('添加3级类目%s成功' % cate3.name)

                    # 获取第四层类目
                    lv4_html = tools.get_html_brower(cate3.url)
                    lv4_data = get_lv(lv4_html)
                    if len(lv4_data) > 0:
                        for lv4 in lv4_data:
                            cate4 = Category(
                                name=lv4['name'],
                                url=lv4['url'],
                                level=4,
                                top_id=cate3.id,
                                amz_id=re.search('3A(\d+)&', lv4['url']).group(1)
                            )
                            db.add(cate4)
                            db.commit()
                            tools.log('添加4级类目%s成功' % cate4.name)

                            # 获取第5层类目
                            lv5_html = tools.get_html_brower(cate4.url)
                            lv5_data = get_lv(lv5_html)
                            if len(lv5_data) > 0:
                                for lv5 in lv5_data:
                                    cate5 = Category(
                                        name=lv5['name'],
                                        url=lv5['url'],
                                        level=5,
                                        top_id=cate4.id,
                                        amz_id=re.search('3A(\d+)&', lv5['url']).group(1)
                                    )
                                    db.add(cate5)
                                    db.commit()
                                    tools.log('添加5级类目%s成功' % cate5.name)

                                    # 获取第6层类目
                                    lv6_html = tools.get_html_brower(cate5.url)
                                    lv6_data = get_lv(lv6_html)
                                    if len(lv6_data) > 0:
                                        for lv6 in lv6_data:
                                            cate6 = Category(
                                                name=lv6['name'],
                                                url=lv6['url'],
                                                level=6,
                                                top_id=cate5.id,
                                                amz_id=re.search('3A(\d+)&', lv6['url']).group(1)
                                            )
                                            db.add(cate6)
                                            db.commit()
                                            tools.log('添加6级类目%s成功' % cate6.name)

                                            # 获取第7层类目
                                            lv7_html = tools.get_html_brower(cate6.url)
                                            lv7_data = get_lv(lv7_html)
                                            if len(lv7_data) > 0:
                                                for lv7 in lv7_data:
                                                    cate7 = Category(
                                                        name=lv7['name'],
                                                        url=lv7['url'],
                                                        level=7,
                                                        top_id=cate6.id,
                                                        amz_id=re.search('3A(\d+)&', lv7['url']).group(1)
                                                    )
                                                    db.add(cate7)
                                                    db.commit()
                                                    tools.log('添加7级类目%s成功' % cate7.name)

                                                    # 获取第8层类目
                                                    lv8_html = tools.get_html_brower(cate7.url)
                                                    lv8_data = get_lv(lv8_html)
                                                    if len(lv8_data) > 0:
                                                        for lv8 in lv8_data:
                                                            cate8 = Category(
                                                                name=lv8['name'],
                                                                url=lv8['url'],
                                                                level=8,
                                                                top_id=cate7.id,
                                                                amz_id=re.search('3A(\d+)&', lv8['url']).group(1)
                                                            )
                                                            db.add(cate8)
                                                            db.commit()
                                                            tools.log('添加8级类目%s成功' % cate8.name)

                                                            # 获取第9层类目
                                                            lv9_html = tools.get_html_brower(cate8.url)
                                                            lv9_data = get_lv(lv9_html)
                                                            if len(lv9_data) > 0:
                                                                for lv9 in lv9_data:
                                                                    cate9 = Category(
                                                                        name=lv9['name'],
                                                                        url=lv9['url'],
                                                                        level=9,
                                                                        top_id=cate8.id,
                                                                        amz_id=re.search('3A(\d+)&', lv9['url']).group(
                                                                            1)
                                                                    )
                                                                    db.add(cate9)
                                                                    db.commit()
                                                                    tools.log('添加9级类目%s成功' % cate9.name)


def get_lv(html):
    doc = pq(html)
    lv_count = doc.find('#leftNav>ul:first>ul li a').size()
    lv = doc.find('#leftNav>ul:first>ul li a').items()
    if lv_count == 0:
        lv = doc.find('#departments>ul:first>ul li a').items()
    data = []
    if lv_count > 0:
        for i in lv:
            url = i.attr('href')
            if 'https://www.amazon.com.au' not in url:
                url = www + url
            level = dict()
            level['url'] = url
            level['name'] = i.text()
            data.append(level)
    return data

