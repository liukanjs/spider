# coding:utf-8
''' 百度ai接口，用来识别验证码等,50000次/天免费
 tesseract文字识别示例：pip install baidu-aip
from PIL import Image
import pytesseract
file_path = basedir + '\\img\\' + file
img = Image.open(file_path)
word = pytesseract.image_to_string(img)
'''

from aip import AipOcr

class BaiDuAI:
    APP_ID = '17027291'
    API_KEY = 'HZkqKI3AsfTscutuGmQF9Teh'
    SECRET_KEY = 'RDobc3B3YMNepE7B6pkmQwfZfgGdSdQc'
    client = None

    def __init__(self):
        self.client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def get_file_content(self, filePath):
        '''
        :param filePath: 本地图片地址
        :return:
        '''
        with open(filePath, 'rb') as fp:
            return fp.read()

    def orc_img(self, imgpath, type='url'):
        '''
        :param imgpath:
        :param type: url:远程图片,file：本地图片
        :return:
        '''
        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"

        if type == 'url':
            image = self.client.basicGeneralUrl(imgpath, options)
        else:
            image = self.get_file_content(imgpath)
            image = self.client.basicGeneral(image)

        return image
