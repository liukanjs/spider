# coding: utf-8

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import redis, pymongo

# 项目根目录
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 数据模型基类
Base = declarative_base()

# # 初始化数据库连接:
DB_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'beauty.db'))
engine = create_engine(DB_URI, connect_args={'check_same_thread': False})

# # 绑定sqlite数据库对象
Session = sessionmaker(bind=engine)
db = Session()

# 绑定MYSQL数据库对象
# engine = create_engine("mysql+pymysql://amz:57f2@GAGA3a2AF213@57f2377d46467.gz.cdb.myqcloud.com:17887/amazon",
#                        max_overflow=5)
# Session = sessionmaker(bind=engine)
# db = Session()

# redis队列
r = redis.Redis(host='120.24.39.11', port='6379', password='redis')

# pymongo 数据库
mongodb = pymongo.MongoClient("mongodb://120.24.39.11:32017/")
mydb = mongodb["beauty"]


class DbTools():
    mgdb = None

    def __init__(self, dbname):
        self.mgdb = mongodb[dbname]

    def add_to_mongo(self, table, result):
        # 直接插入数据
        try:
            if self.mgdb[table].insert_one(result):
                # print('存储到MONGODB成功')
                pass
        except Exception as e:
            print('存储到mongo出错：%s' % e)

    def update_to_mongo(self, table, query, update):
        # 避免重复插入数据
        # query = {'lv2_title': lv2_title}
        # update_to_mongo('category', query, category)
        try:
            if self.mgdb[table].update_one(query, {'$set': update}, True):
                # log('记录数：%s' % (db[table].count_documents({})))
                pass
        except Exception as e:
            print('存储到mongo出错：%s' % e)
