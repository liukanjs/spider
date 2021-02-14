from app import db
from app.models import Category, Product
import redis, json

'''
用于向redis分发采集任务
'''
r = redis.Redis(host='120.24.39.11', port='6379', password='redis')


def last_category():
    # 输出各个类目的最底层
    # print(db.query(Category).filter(Category.top_id == 4558).first())
    # print(db.query(Category).get(2).to_dict())

    last_category = []
    cate = db.query(Category).all()
    for i in cate:
        item = i.to_dict()
        sql = db.query(Category).filter(Category.top_id == str(item['id'])).first()
        if sql is None:
            url = item['url']
            cid = item['id']
            task = dict(
                cid=cid,
                url=url
            )
            task = json.dumps(task)
            last_category.append(task)
            r.sadd('amz_task_url', task)  # 任务url添加到redis队列
    return last_category


if __name__ == '__main__':
    r.delete('amz_task_url')
    catelist = last_category()
    print(len(catelist))
