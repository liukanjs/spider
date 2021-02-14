# coding:utf8
# 密码字典
import os, sys, random
from xpinyin import Pinyin
import itertools as its

p = Pinyin()
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class PasswordDict(object):
    MOST_USE = []  # 常用密码
    # 年：1970-2020
    YEAR = ['1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982',
            '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
            '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
            '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021',
            '2022', '2023', '2024', '2025']
    # 月：01-12
    MOTH = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    # 日:01-31
    DAY = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
           '19',
           '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    # 常用特殊字符
    MOST_SIN = ['!', '*', '#', '_', '@']

    # 常见姓氏拼音
    FNAMA = ['li', 'wang', 'zhang', 'liu', 'chen', 'yang', 'zhao', 'huang', 'zhou', 'wu', 'xu', 'sun', 'hu', 'zhu',
             'gao', 'lin', 'he', 'guo', 'ma', 'luo', 'liang', 'song', 'zheng', 'xie', 'han', 'tang', 'feng', 'yu',
             'dong', 'xiao', 'cheng', 'cao', 'yuan', 'deng', 'xu', 'fu', 'shen', 'ceng', 'peng', 'lv', 'su', 'lu',
             'jiang', 'cai', 'jia', 'ding', 'wei', 'xue', 'ye', 'yan', 'yu', 'pan', 'du', 'dai', 'xia', 'zhong', 'wang',
             'tian', 'ren', 'jiang', 'fan', 'fang', 'shi', 'yao', 'tan', 'liao', 'zou', 'xiong', 'jin', 'lu', 'hao',
             'kong', 'bai', 'cui', 'kang', 'mao', 'qiu', 'qin', 'jiang', 'shi', 'gu', 'hou', 'shao', 'meng', 'long',
             'wan', 'duan', 'cao', 'qian', 'tang', 'yin', 'li', 'yi', 'chang', 'wu', 'qiao', 'he', 'lai', 'gong', 'wen']
    # 所有可以组成名字首字母的字母
    LNAME = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 's', 't', 'w', 'x', 'y',
             'z']
    # 包含名字中字的所有拼音
    NAMELIST = []
    B_SUB = ['bo', 'bi', 'bai', 'bei', 'bao', 'ban', 'ben', 'bin', 'bang', 'bing', 'biao']
    C_SUB = ['ci', 'cai', 'can', 'cen', 'cun', 'ceng', 'cong']
    D_SUB = ['de', 'di', 'du', 'dai', 'dao', 'dan', 'deng', 'ding', 'dong']
    F_SUB = ['fa', 'fu', 'fei', 'fan', 'fen', 'feng', 'fang', 'fing']
    G_SUB = ['gu', 'gui', 'gao', 'gan', 'gen', 'guo', 'gang', 'geng', 'guan', 'guang']
    H_SUB = ['hu', 'hui', 'hao', 'han', 'hen', 'huo', 'hang', 'heng', 'huan', 'huang']
    J_SUB = ['ji', 'jiu', 'ju', 'jie', 'jin', 'jun', 'jue', 'jing', 'jia', 'jiao', 'jian', 'juan']
    K_SUB = ['kai', 'kun', 'kan', 'kun', 'kuo', 'kang', 'kong', 'kuan', 'kuang']
    L_SUB = ['le', 'li', 'lu', 'lai', 'lei', 'lan', 'lin', 'lun', 'lang', 'ling', 'long', 'liao', 'lian', 'luan']
    M_SUB = ['mi', 'mu', 'mai', 'mei', 'mao', 'miu', 'man', 'min', 'mang', 'meng', 'ming', 'miao', 'mian']
    N_SUB = ['na', 'ni', 'niu', 'nie', 'nan', 'nuo', 'neng', 'ning']
    P_SUB = ['pi', 'pu', 'pai', 'pei', 'pan', 'pin', 'pang', 'peng', 'ping', 'pian']
    Q_SUB = ['qi', 'qiu', 'qing', 'qiang', 'quan', 'qian']
    S_SUB = ['sa', 'so', 'se', 'si', 'su', 'sai', 'suo', 'sang', 'song']
    T_SUB = ['ta', 'to', 'te', 'ti', 'tu', 'tai', 'tao', 'tan', 'tuo', 'tang', 'teng', 'ting', 'tong', 'tian']
    W_SUB = ['wa', 'wo', 'wai', 'wei', 'wang', 'wan']
    X_SUB = ['xi', 'xu', 'xv', 'xie', 'xin', 'xun', 'xue', 'xing', 'xiang', 'xiong', 'xia', 'xian', 'xuan']
    Y_SUB = ['ya', 'yi', 'yu', 'yao', 'yan', 'yun', 'yue', 'ying', 'yang', 'yong', 'yia', 'yuan']
    Z_SUB = ['zu', 'zao', 'zan', 'zun', 'zuo', 'zeng', 'zong']
    ZH_SUB = ['zhi', 'zhou', 'zhan', 'zhen', 'zhong', 'zhuan']
    CH_SUB = ['cha', 'che', 'chi', 'chu', 'chai', 'chao', 'chan', 'chen', 'chong', 'chuang']
    SH_SUB = ['sha', 'shi', 'shu', 'shao', 'shou', 'shan', 'shen', 'shuo', 'shuang']

    def __init__(self):
        self.MOST_USE = [i for i in self.open_file(basedir + '/data/6000常用密码字典.txt').split('\r\n')]
        self.NAMELIST = self.__namelist()

    def __namelist(self):
        nl = []
        nl.extend(self.B_SUB)
        nl.extend(self.C_SUB)
        nl.extend(self.D_SUB)
        nl.extend(self.F_SUB)
        nl.extend(self.G_SUB)
        nl.extend(self.H_SUB)
        nl.extend(self.J_SUB)
        nl.extend(self.K_SUB)
        nl.extend(self.L_SUB)
        nl.extend(self.M_SUB)
        nl.extend(self.N_SUB)
        nl.extend(self.P_SUB)
        nl.extend(self.Q_SUB)
        nl.extend(self.S_SUB)
        nl.extend(self.T_SUB)
        nl.extend(self.W_SUB)
        nl.extend(self.X_SUB)
        nl.extend(self.Y_SUB)
        nl.extend(self.Z_SUB)
        nl.extend(self.ZH_SUB)
        nl.extend(self.CH_SUB)
        nl.extend(self.SH_SUB)
        return nl

    def get_most_password(self):
        # 常用密码
        return self.MOST_USE

    def get_esay_password(self, min, max):
        '''
        # 弱密码，连号/同号数字/字母，生日，手机号，名字（拼音或首字母）+生日（年/月日），QQ号，
        :param min: 密码最小长度
        :param max:密码最大长度
        :return:返回密码数组
        '''
        words = '1234567890qwertyuiopasdfghjklzxcvbnm@#!*&'
        passwords = []
        date = []
        # 同号字符串
        for word in words:
            for n in range(min, max + 1):
                keys = [i for i in its.product(word, repeat=n)]
                for key in keys:
                    passwords.append(''.join(key))

        # 连号字符串
        w = words + words
        for i in range(0, len(words)):
            for k in range(min, max + 1):
                passwords.append(w[i:i + k])

        # 生日,年+月+日
        for day in self.DAY:
            for moth in self.MOTH:
                for year in self.YEAR:
                    passwords.append(year + moth + day)

        # 生日,月+日
        for moth in self.MOTH:
            for year in self.YEAR:
                passwords.append(year + moth + day)

        # 名字拼音,2个字或3个字,3994642个字典
        for lastname in self.NAMELIST:
            for midname in self.NAMELIST:
                for firstname in self.FNAMA:
                    fullname_2 = firstname + lastname
                    fullname_3 = firstname + midname + lastname
                    # passwords.append(fullname_2)
                    # passwords.append(fullname_3)

        # 手机号13xxxxxxxx
        # for i in range(3, 9):
        #     if i == 4:
        #         pass
        #     else:
        #         head = '1' + str(i)
        #         for n in its.product('0123456789', repeat=8):
        #             date.append(head.join(n))

        return list(set(passwords))

    def get_random_password(self, min, max):
        """
        :param min_digits: 密码最小长度
        :param max_digits: 密码最大长度
        :param words: 密码可能涉及的字符
        :return: 密码生成器
        """
        pd = []
        words = '0123456789abcdefghijklmnopqrstuvwxyz@#!*'
        while min <= max:
            pwds = its.product(words, repeat=min)
            for i in pwds:
                pd.append(''.join(i))
            min += 1
        return pd

    def open_file(self, path):
        try:
            fp = open(path, 'rb')
            html = fp.read().decode('utf-8')
            return html
        except Exception as e:
            print(e)

    def save_file(self, filename, content):
        try:
            file_path = basedir + '/data/'
            if not os.path.exists(file_path):
                # 判断目录是否存在，否则创建并给与权限
                os.makedirs(file_path)
                os.chmod(file_path, os.stat.S_IRWXU)  # 拥有着的读写权限
            with open(file_path + filename, 'a+', encoding='utf8') as f:
                f.write(content)
        except Exception as e:
            print(e)


'''
ps = PasswordDict()
add = ps.get_esay_password(6, 12)
print(add)
print(len(add))


str = '李王张刘陈杨赵黄周吴徐孙胡朱高林何郭马罗梁宋郑谢韩唐冯于董萧程曹袁邓许傅沈曾彭吕苏卢蒋蔡贾丁魏薛叶阎余潘杜戴夏钟汪田任姜范方石姚谭廖邹熊金陆郝孔白崔康毛邱秦江史顾侯邵孟龙万段漕钱汤尹黎易常武乔贺赖龚文'
ads=[]
for i in str:
    ads.append(p.get_pinyin(i, ''))
print(ads)
'''
