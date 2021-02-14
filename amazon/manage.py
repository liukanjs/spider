from app.models import init_db
from app.get_product import main
import threading, time
from app.get_product_brower import main as get_product_brower

if __name__ == '__main__':
    start = time.time()
    # main()
    get_product_brower()
    end = time.time()
    print("运行时长 : %.03f 秒" % (end - start))

    # try:
        # 初始化数据库
        # init_db()
        # # 初始化代理池
        # th1 = threading.Thread(target=run_ips)
        # th1.setDaemon(True)
        # th1.start()

    # 多线程执行产品采集程序

    # except Exception as e:
    #     print('出错位置：manage.py')
    #     print(e)
    #     end = time.clock()
    #     print("运行时长 : %.03f 秒" % (end - start))
