# -*- coding: utf-8 -*-
# 爬取艾美e族的产品信息
import requests
from bs4 import BeautifulSoup
import json
import random
import time
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


# 日志输出
def log(event):
    times = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    with open('./log/' + today + '.log', 'a+') as f:
        f.write(times + event + '\n')
    print(times + event)


# 邮件提醒
def mail(title, info):
    my_sender = '54191225@qq.com'  # 发件人邮箱账号
    my_pass = ''  # 发件人邮箱密码
    my_user = ''  # 收件人邮箱账号，我这边发送给自己
    ret = True
    try:
        msg = MIMEText(info, 'plain', 'utf-8')
        msg['From'] = formataddr(["Ken爬虫", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["Ken", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = title  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


def get_proxy_ip():
    # 获取代理ip地址及端口
    log(' 采集代理ip')
    ip_list = []
    proxy_url = 'https://cn-proxy.com/'
    html = requests.get(proxy_url).text
    soup = BeautifulSoup(html, 'lxml')
    ipbody = soup.find_all('tbody')
    iptrs = ipbody[1].find_all('tr')
    for i in iptrs:
        tds = i.find_all('td')
        ip_list.append(tds[0].text + ':' + tds[1].text)
    log(' 成功采集%s个代理ip地址' % (len(ip_list)))
    return ip_list


def get_random_ip(ip_list):
    # 随机生成一条代理ip地址
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    log(' 代理ip地址为:%s' % (proxies))
    return proxies


def payloadHeader(store_id):
    # 设置请求头
    userAgent = ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
                 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
                 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
                 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)']
    referer_url = 'https://h5.amez999.com/storeDetail?shopId=%s' % (store_id)
    headers = {
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://h5.amez999.com',
        'user-agent': random.choice(userAgent),
        'referer': referer_url
    }
    return headers


def get_store_id():
    url = 'https://gateway.amez999.com/web/user/search/likeShopInfo'
    payloadData = {
        'entity': {},
        'pageNo': 1,
        'pageSize': 100,
        'searchContent': '""'
    }
    headers = {
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://amez999.com',
        'user-agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
        'referer': 'https://amez999.com/searchResult?keyword=&type=2&navIndex=1'
    }
    store_list = requests.post(url, payloadData, headers)


def payloadData(store_id):
    # 根据店铺id的请求字段
    payloadData = {
        'entity': {'shopId': store_id},
        'pageNo': 1,
        'pageSize': 100
    }

    log(' 采集店铺id:%s' % (store_id))
    return payloadData


def get_goods_data(store_id, proxies):
    # 商品接口地址
    all_goods_url = "https://gateway.amez999.com/mobile/user/userShop/allGoods"
    # 获取商品信息
    goods = requests.post(all_goods_url, data=json.dumps(payloadData(store_id)), headers=payloadHeader(store_id),
                          proxies=proxies, timeout=30).json()
    log(' 采集商品%s条' % (goods['data']['total']))
    return goods


def save_data(goods_json):
    # 保存数据到数据库
    conn = pymysql.connect(
        host='localhost',  # mysql服务器地址
        port=3306,  # 端口号
        user='root',  # 用户名
        passwd='root',  # 密码
        db='amdb',  # 数据库名称
        charset='utf8',  # 连接编码，根据需要填写
    )
    cur = conn.cursor()  # 创建并返回游标

    for line in goods_json['data']['content']:
        if 'evaluateNum' not in line:
            line['evaluateNum'] = 0
        if 'goodsRate' not in line:
            line['goodsRate'] = 0

        times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        goodsBody = line["goodsBody"]
        goodsBody = goodsBody.replace("\'", '"')

        sql = "INSERT INTO `amdb`.`amgoods` (`pid`, `actTitle`, `activitys`, `allowVat`, `areaId1`, `areaId2`, `brandId`, `brandName`, `category1`, `category2`, `category3`, `createTime`, `evaluateNum`, `freightTemplateId`, `goodsBody`, `goodsName`, `goodsRate`, `goodsSaleNum`, `goodsState`, `goodsStorage`, `goodsVerify`, `imageUrl`, `isDelete`, `isOverseasPurchase`, `isPointsGoods`, `jingle`, `marketPrice`, `mobileBody`, `originalPrice`, `promotionDiscountRate`, `shopId`, `shopName`, `getTime`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            line["id"], line["actTitle"], line["activitys"], line["allowVat"], line["areaId1"], line["areaId2"],
            line["brandId"], line["brandName"].replace("\'", '"'), line["category1"], line["category2"],
            line["category3"],
            line["createTime"],
            line["evaluateNum"], line["freightTemplateId"], goodsBody, line["goodsName"].replace("\'", '"'),
            line["goodsRate"],
            line["goodsSaleNum"], line["goodsState"], line["goodsStorage"], line["goodsVerify"],
            line["imageUrl"].replace("\'", '"'),
            line["isDelete"], line["isOverseasPurchase"], line["isPointsGoods"], line["jingle"].replace("\'", '"'),
            line["marketPrice"],
            line["mobileBody"].replace("\'", '"'), line["originalPrice"], line["promotionDiscountRate"], line["shopId"],
            line["shopName"].replace("\'", '"'),
            times)
        # log(" 开始保存数据至mysql数据库")
        try:
            cur.execute(sql)
            # log(" 数据存储成功")
        except:
            cur.rollback()
            log(" 数据存储失败")
    conn.close()


def save_goods_data(store_id, proxies):
    # 提取数据并保存到mysql
    goods_data = get_goods_data(store_id, proxies)
    if goods_data['data']['total'] > 0:
        save_data(goods_data)
    else:
        log(' 店铺关闭或无上架商品')


def store_id_list(proxies):
    url = 'https://gateway.amez999.com/web/user/search/likeShopInfo'
    payloadData = {
        'entity': {},
        'pageNo': 1,
        'pageSize': 500,
        'searchContent': ''
    }
    headers = {
        'content-type': 'application/json',
        'origin': 'https://amez999.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'referer': 'https://amez999.com/searchResult?keyword=&type=2&navIndex=1',
        'x-requested-with': 'XMLHttpRequest'
    }
    store_list = requests.post(url, headers=headers, data=json.dumps(payloadData), proxies=proxies, timeout=30).json()
    store_id = []

    for i in store_list['data']['content']:
        store_id.append(i['id'])

    log(' 获取到%s个店铺id' % (len(store_id)))

    store_id.sort()
    return store_id


def main():
    # 设置代理ip
    ip_list = get_proxy_ip()
    proxies = get_random_ip(ip_list)
    # 设定采集店铺数量，采集店铺全部产品并保存至mysql
    store_list = store_id_list(proxies)

    for store_id in store_list:
        proxies = get_random_ip(ip_list)
        log('------开始采集%s号店铺------' % (store_id))
        try:
            save_goods_data(store_id, proxies)
            log(' %s号店铺采集成功！' % (store_id))
        except Exception as e:
            log(' 采集&存储错误：%s' % (e))
        time.sleep(1)

    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_info = open('./log/' + today + '.log', 'r')
    info = log_info.read()
    res = mail(today + '爬虫日志', info)
    log_info.close()
    if res:
        print("邮件发送成功")
    else:
        print("邮件发送失败")


if __name__ == '__main__':
    main()
