# coding: utf-8

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import redis

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 数据模型基类
Base = declarative_base()

# # 初始化数据库连接:
# DB_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'amz.db'))
# engine = create_engine(DB_URI, connect_args={'check_same_thread': False})
#
# # 绑定sqlite数据库对象
# Session = sessionmaker(bind=engine)
# db = Session()

# 绑定MYSQL数据库对象
engine = create_engine("mysql+pymysql://amz:57f2@GAGA3a2AF213@57f2377d46467.gz.cdb.myqcloud.com:17887/amazon",
                       max_overflow=5)
Session = sessionmaker(bind=engine)
db = Session()


r = redis.Redis(host='120.24.39.11', port='6379', password='redis')
