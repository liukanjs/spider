# coding:utf-8
import os, stat, time, requests, pyquery, random, datetime, json, redis, re
from app import basedir
from fake_useragent import UserAgent
from requests.exceptions import RequestException
from app import r
from pyquery import PyQuery as pq
from app.baiduai import BaiDuAI

ai = BaiDuAI()


# r = redis.Redis(host='120.24.39.11', port='6379', password='redis')


class Tools:
    cookies = {}
    proxies = {}

    def __init__(self, has_cookie=False):
        self.proxies = self.get_proxies()
        if has_cookie:
            self.cookies = self.get_cookie()
            print(self.cookies)

    def set_pro_cok(self):
        self.proxies = self.get_proxies()
        self.cookies = self.get_cookie()

    def get_cookie(self):
        try:
            s = requests.session()
            s.get('https://www.amazon.com.au', headers=self.randHeader(), proxies=self.proxies, timeout=10)
            cookies = requests.utils.dict_from_cookiejar(s.cookies)
            print(cookies)
            return cookies
        except Exception as e:
            self.log('出错位置：tools.get_cookie')
            print(e)
            return {}

    def get_proxies(self):
        try:
            proxies = json.loads(r.srandmember('proxy_ip'))
            # proxies = json.loads(requests.get('http://127.0.0.1:5000/get_ip', timeout=20).text)
            # if 'http' not in proxies:
            #     proxies = {}
            print(proxies)
            return proxies
        except Exception as e:
            self.log('出错位置：tools.get_proxies')
            print(e)
            return {}

    # 日志输出
    def log(self, event):
        times = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        log_path = basedir + '/log/'
        log_name = str(log_path + today) + '_amazon.log'
        if not os.path.exists(log_path):
            # 判断目录是否存在，否则创建并给与权限
            os.makedirs(log_path)
            os.chmod(log_path, stat.S_IRWXU)  # 拥有着的读写权限
        with open(log_name, 'a+', encoding='utf8') as f:
            f.write(str(times + event) + '\n')
        print(times + event)

    def get_html_req(self, url):
        time.sleep(random.randint(3, 5))
        now_minute = datetime.datetime.now().minute
        if (now_minute % 3) == 2:  # 4分钟更换一次代理和cokkie
            self.proxies = self.get_proxies()
            self.cookies = self.get_cookie()
            self.log('更换代理及cookie')
        try:
            r = requests.get(url, timeout=10, headers=self.randHeader(), cookies=self.cookies, proxies=self.proxies)
            r.encoding = r.apparent_encoding
            retry = 0
            if r.status_code == 200:
                html = r.text
                if self.check_captcha(html):
                    return self.check_captcha(html)
                return html
            else:
                retry += 1
                self.log('打开网页出错，切换代理重试%s次' % retry)
                time.sleep(10)
                self.proxies = self.get_proxies()
                self.cookies = self.get_cookie()
                self.get_html_req(url)
                if retry > 10:
                    self.log('重试10次失败，程序终止')
                    r.raise_for_status()
        except RequestException as e:
            print('出错位置：tools.get_html_req')
            print(e)
            return ''

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

    def open_file(self, path):
        try:
            fp = open(path, 'rb')
            html = fp.read().decode('utf-8')
            return html
        except Exception as e:
            print(e)

    def save_file(self, filename, content):
        try:
            file_path = basedir + '/html/'
            if not os.path.exists(file_path):
                # 判断目录是否存在，否则创建并给与权限
                os.makedirs(file_path)
                os.chmod(file_path, stat.S_IRWXU)  # 拥有着的读写权限
            with open(file_path + filename, 'a+', encoding='utf8') as f:
                f.write(content)
        except Exception as e:
            print(e)

    def download(self, link):
        filename = re.findall(r'.*/(.+)', link)[0]
        filename = str(int(time.time())) + '_' + filename
        file_path = basedir + '/html/'
        if not os.path.exists(file_path):
            # 判断目录是否存在，否则创建并给与权限
            os.makedirs(file_path)
            os.chmod(file_path, stat.S_IRWXU)  # 拥有着的读写权限
        try:
            pic = requests.get(link, timeout=30, headers=self.randHeader(), cookies=self.cookies,
                               proxies=self.proxies)
            if pic.status_code == 200:
                with open(os.path.join(file_path) + os.sep + filename, 'wb') as fp:
                    fp.write(pic.content)
                    fp.close()
            print("下载完成:%s" % filename)
            return os.path.join(file_path) + os.sep + filename
        except Exception as e:
            print(e)

    def check_captcha(self, html):
        is_ok = False
        doc = pq(html)
        # 判断是否抓取到了数据，否则会有验证码验证页
        for i in doc.find('h4').items():
            if 'Server Busy' in i.text():
                self.log('需要输入验证码')
                characters = doc('img').attr('src')  # 验证码图片
                characters = self.download(characters)
                time.sleep(2)
                if characters:
                    captcha = ai.orc_img(imgpath=characters, type='file')  # 识别验证码
                    try:
                        captcha = captcha['words_result'][0]['words']
                        self.log('验证码为：' + captcha)
                        payload = {
                            'amzn': doc.find("input[name='amzn']").attr('value'),
                            'amzn-r': doc.find("input[name='amzn-r']").attr('value'),
                            'field-keywords': captcha
                        }

                        url = 'https://www.amazon.com.au/errors/validateCaptcha'
                        r = requests.get(url, params=payload, timeout=10, headers=self.randHeader(),
                                         cookies=self.cookies,
                                         proxies=self.proxies)
                        self.log('发送验证码url：%s' % r.url)
                        if r.status_code == 200:
                            self.log('验证码提交')
                            self.save_file(str(random.randint(1, 10000)) + '_code.html', r.text)
                            return r.text
                        else:
                            self.log('认证失败')
                    except Exception as e:
                        print(e)
                is_ok = False
        return is_ok
