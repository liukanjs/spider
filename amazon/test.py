# from app.get_product_brower import main as get_product_brower
from app.baiduai import BaiDuAI
from app import basedir
import os
from PIL import Image
import pytesseract


def file_name(file_dir):
    return os.listdir(file_dir)


if __name__ == '__main__':
    # get_product_brower()
    ai = BaiDuAI()

    result = ai.orc_img(imgpath='https://images-na.ssl-images-amazon.com/captcha/qamfifum/Captcha_dxelsdobyw.jpg', type='url')
    # word2 = result['words_result'][0]['words']
    print(result)
    # print('tesseract:%s,baidu:%s' % (word, word2))

    for file in file_name(basedir + '\\img\\'):
        file_path = basedir + '\\img\\' + file
        img = Image.open(file_path)
        word = pytesseract.image_to_string(img)

        result = ai.orc_img(imgpath=basedir + '/img/' + file, type='file')
        word2 = result['words_result'][0]['words']
        print('tesseract:%s,baidu:%s' % (word, word2))
