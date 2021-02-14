# coding=utf8

import random, requests, hashlib, time
from urllib import parse

def md5(s):
    m = hashlib.md5()
    m.update(s.encode(encoding='UTF-8'))
    return m.hexdigest()


def fanyi(keyword):
    appid = '20190813000326267'  # 你的appid
    secretKey = '4O9PzAHHLXHuiJM1HFXB'  # 你的密钥

    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    q = parse.quote(keyword)
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = appid + keyword + str(salt) + secretKey
    sign = md5(sign)
    myurl = myurl + '?appid=' + appid + '&q=' + q + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    trans_result = ''
    try:
        result = requests.get(myurl, timeout=10)
        if result.status_code == 200:
            data = result.json()
            print(data)
            trans_result = data['trans_result'][0]['dst']
    except Exception as e:
        print(e)
    time.sleep(1)
    return trans_result


if __name__ == '__main__':
    fanyi('苹果')
