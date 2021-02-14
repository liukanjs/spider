# coding:utf-8
# 代理ip池
import time, redis, random, json, requests, threading, os, re
from apscheduler.schedulers.blocking import BlockingScheduler
from pyquery import PyQuery as pq
from fake_useragent import UserAgent

r = redis.Redis(host='120.24.39.11', port='6379', password='redis')
scheduler = BlockingScheduler()


class Proxy:
    ip = {}
    ips = None

    # def __init__(self):
    #     # self.ips = self.get_proxy_ip()

    # 生成随机头
    def randHeader(self):
        head_connection = ['Keep-Alive', 'close']
        head_accept = ['text/html, application/xhtml+xml, */*']
        head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
        header = {
            'Connection': head_connection[0],
            'Accept': head_accept[0],
            'Accept-Language': head_accept_language[1],
            'User-Agent': str(UserAgent().random)
        }
        return header

    def get_ip(self):
        # 随机获取ip
        proxy_ip = json.loads(r.srandmember('proxy_ip'))
        if proxy_ip is None:
            proxy_ip = {}
        return proxy_ip

    def get_url(self, url):
        try:
            result = requests.get(url=url, timeout=10, headers=self.randHeader())
            result.encoding = result.apparent_encoding
            if result.status_code == 200:
                return result.text
        except Exception as e:
            print(e)

    def ip_kuaidaili(self):
        # 快代理ip
        try:
            url = 'https://www.kuaidaili.com/free/'
            html = self.get_url(url)
            doc = pq(html)
            for tr in doc.find('table.table>tbody>tr').items():
                proxie = {}
                ip = tr.find('td').eq(0).text()
                port = tr.find('td').eq(1).text()
                htype = tr.find('td').eq(3).text()
                is_ok = tr.find('td').eq(2).text()
                if is_ok == '高匿名':
                    if htype == 'HTTP':
                        proxie['http'] = 'http://%s:%s' % (ip, port)
                    else:
                        proxie['https'] = 'https://%s:%s' % (ip, port)
                        if self.check_proxy_ip(proxie, ip['ip']):
                            print('有效ip：%s,验证成功,添加到队列' % proxie)
                            r.sadd('proxy_ip', json.dumps(proxie))
        except Exception as e:
            print(e)
            print('错误位置：ip_kuaidaili')

    def ip_66ip(self):
        pass

    def get_proxy_ip(self, max_ip=10):
        # 透明代理ip，无效，需要高匿名ip
        try:
            url = 'http://ip.jiangxianli.com/api/proxy_ips'
            ips = json.loads(requests.get(url, timeout=10).text)
            proxies = []
            if ips['code'] == 0:
                for ip in ips['data']['data']:
                    if ip['anonymity'] >= 1:  # 高匿名ip：2，匿名=1，透明=0
                        proxie = {}
                        if ip['protocol'] == 'http':
                            proxie['http'] = '%s:%s' % (ip['ip'], ip['port'])
                        elif ip['protocol'] == 'https':
                            proxie['https'] = '%s:%s' % (ip['ip'], ip['port'])
                        # 验证代理ip
                        if self.check_proxy_ip(proxie, ip['ip']):
                            print('有效ip：%s,验证成功,添加到队列' % proxie)
                            proxies.append(proxie)
                            r.sadd('proxy_ip', json.dumps(proxie))
            if len(proxies) > max_ip:
                return proxies
            else:
                self.get_proxy_ip()
        except Exception as e:
            # print(e)
            self.get_proxy_ip()

    def check_proxy_ip(self, proxies, old_ip):
        is_ok = False
        TEST_URL = 'http://diymeir.com:5001'
        try:
            requests.packages.urllib3.disable_warnings()
            response = requests.get(TEST_URL, proxies=proxies, verify=False, timeout=5)
            if response.status_code == 200:
                # print('ip可连接，返回值是%s，old_ip：%s' % (response.text, old_ip))
                if old_ip == response.text:
                    is_ok = True
        except Exception as e:
            # print(e)
            pass
        return is_ok

    def check_redis(self):
        ips = r.smembers('proxy_ip')
        if len(ips) > 0:
            for i in ips:
                # 遍历所有ip
                proxy_ip = i
                reg = "\d+\.\d+\.\d+\.\d+"
                ip = re.search(reg, str(i)).group()
                proxy_ip = json.loads(proxy_ip)
                # 验证代理ip
                if self.check_proxy_ip(proxy_ip, ip) is False:
                    # 删除一条数据
                    print('无效ip：%s，删除！' % proxy_ip)
                    delrow = r.srem('proxy_ip', json.dumps(proxy_ip))
        else:
            self.get_proxy_ip()


# 初始化ip池
proxy = Proxy()


def task():
    # 定时采集ip池
    scheduler.add_job(proxy.get_proxy_ip, trigger='interval', seconds=90, max_instances=10)
    # scheduler.add_job(proxy.ip_kuaidaili, trigger='interval', seconds=30, max_instances=10)

    # 定时维护ip池
    scheduler.add_job(proxy.check_redis, trigger='interval', seconds=90, max_instances=10)

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    task()
