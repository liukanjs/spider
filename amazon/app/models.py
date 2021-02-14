from app import Base, engine
from sqlalchemy import ForeignKey, Table
from sqlalchemy import Column, String, Integer, Text, DateTime, Float, Boolean,BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime


def to_dict(self):
    return {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns}


Base.to_dict = to_dict


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, index=True)
    age = Column(Integer)
    addtime = Column(DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)


class Category(Base):
    # 类目
    __tablename__ = 'amz_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    sub_name = Column(String(64), index=True)
    amz_id = Column(BigInteger)  # 亚马逊类目id
    url = Column(Text)
    level = Column(Integer)  # 类目级别
    top_id = Column(Integer)  # 上级亚马逊类目id
    addtime = Column(DateTime, index=True, default=datetime.now)  # 添加时间
    # 一对多:
    products = relationship('Product', backref='amz_category')

    def __repr__(self):
        return '<Category %s>' % self.name


class Product(Base):
    # 商品
    __tablename__ = 'amz_product'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)  # 商品名称
    asin = Column(String(64), index=True, unique=True)  # 商品唯一编码
    seller = Column(String(64), index=True)  # 卖家名称
    img = Column(Text)  # 商品图片
    url = Column(Text)  # 商品链接
    price = Column(Float)  # 商品价格
    commentnum = Column(Integer, default=0)  # 评论数
    star = Column(Float, default=0)  # 评分
    offersnum = Column(Integer, default=0)  # 跟卖数
    is_prime = Column(Boolean, default=False)  # 默认不支持prime
    is_amazon = Column(Boolean, default=False)  # 默认非自营商品
    is_best_sellers = Column(Boolean, default=False)  # 默认不是best sellers
    category_id = Column(Integer, ForeignKey('amz_category.id'))  # 类目id，关联类目表
    addtime = Column(DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Product %s>' % self.title

class Review(Base):
    # 商品评价
    __tablename__ = 'amz_review'

    id = Column(Integer, primary_key=True)
    title = Column(String(64), index=True)  # 商品名称
    asin = Column(String(64), index=True, unique=True)  # 商品唯一编码
    customer = Column(String(64), index=True, unique=True)  # 评价用户户
    url = Column(Text)  # 评价页面链接
    price = Column(Float)  # 商品价格
    star = Column(Float, default=0)  # 评分
    category_id = Column(Integer, ForeignKey('amz_category.id'))  # 类目id，关联类目表
    addtime = Column(DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Product %s>' % self.title



def init_db():
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    pass