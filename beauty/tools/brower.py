from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as Foptions
import os, random, time, json, sys
from tools.tools import Tools as tools
from pyquery import PyQuery as pq
from tools.base import r, basedir


class Browser:
    proxies = {}
    driver = {}
    timeout = 10

    def __init__(self):
        # self.proxies = self.get_proxies()
        # self.driver = self.chrome_driver()
        self.driver = self.firefox_driver()

    def get_proxies(self):
        tcp = 'http://'
        proxies = json.loads(r.srandmember('proxy_ip'))
        for i in proxies.keys():
            if i == 'https':
                tcp = 'https://'
        proxies = tcp + proxies['http']
        return proxies

    def chrome_driver(self):
        # 浏览器设置
        options = Options()
        options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
        options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
        options.add_argument('--incognito')  # 隐身模式（无痕模式）
        options.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
        options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')  # 以根用户打身份运行Chrome，使用-no-sandbox标记重新运行Chrome,禁止沙箱启动
        options.add_argument('--disable-gpu')  # 不开启GPU加速
        # options.add_argument("--headless")  # 浏览器不提供可视化页面
        # options.add_argument("--proxy-server=%s" % self.proxies)  # 设置代理地址

        if os.name == 'nt':
            chrome_driver = basedir + "\chromedriver.exe"
        else:
            chrome_driver = "/www/wwwroot/pyweb/chromedriver"

        driver = webdriver.Chrome(options=options, executable_path=chrome_driver)
        driver.set_page_load_timeout(self.timeout)
        driver.implicitly_wait(self.timeout)
        # driver.set_window_size(1440, 900)

        return driver


    def firefox_driver(self):
        # 浏览器设置
        options = Foptions()
        options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
        options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
        options.add_argument('--incognito')  # 隐身模式（无痕模式）
        options.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
        options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')  # 以根用户打身份运行Chrome，使用-no-sandbox标记重新运行Chrome,禁止沙箱启动
        options.add_argument('--disable-gpu')  # 不开启GPU加速
        options.add_argument("--headless")  # 浏览器不提供可视化页面
        # # options.add_argument("--proxy-server=%s" % self.proxies)  # 设置代理地址
        # options.add_argument('Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/12.0 Mobile/15A372 Safari/604.1')   # 手机模拟

        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(self.timeout)
        driver.implicitly_wait(self.timeout)
        driver.set_window_size(1440, 900)

        return driver

    def get_html_brower(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(self.timeout)
            html = self.driver.page_source
            return html
        except Exception as e:
            print('加载超时:%s' % url)
            # self.driver.execute_script("window.stop()")
            # html = self.driver.page_source
            return ''


'''
    示例程序：
from app.brower import Browser
from queue import Queue
import threading, time, random

def open_url(url):
    driver = Browser()
    html = driver.get_html_brower(url)
    print(html)
    time.sleep(5)
    html = driver.get_html_brower(random.choice(urls))


if __name__ == '__main__':
    q = Queue()
    for url in urls:
        q.put(url)
    th1 = threading.Thread(target=open_url, args=(q.get(),))
    th2 = threading.Thread(target=open_url, args=(q.get(),))
    th1.start()
    th2.start()
'''
