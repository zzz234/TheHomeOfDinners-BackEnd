from os import path

import jieba
import numpy

import PIL.Image as image
from rest_framework.pagination import PageNumberPagination
from wordcloud import WordCloud

from TheHomeOfDinners.settings import BASE_DIR


class MyPageNumberPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 10


def generateWordCloud(text, restaurant):
    """
    生成词云
    :param text: 文本
    :param restaurant: 餐馆
    :return: 
    """
    # jieba分词，生成字符串，wordCloud无法直接生成正确的中文词云
    cut_text = " ".join(jieba.cut(text))
    image_path = path.join(BASE_DIR, 'media', 'wordCloud.png')
    color_mask = image.open(image_path)
    color_mask = numpy.array(color_mask)

    wordCloud = WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path=path.join(BASE_DIR, 'media', 'msyh.ttc'),
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=2000,
        # 最大号字体
        max_font_size=100
    )
    # 生成词云
    wordCloud.generate(cut_text)
    # 设置词云图片保存路径
    wordCloud.to_file(path.join(BASE_DIR, 'media', 'wordClouds', restaurant + '.png'))
    return path.join('pictures', 'wordClouds', restaurant + '.png')
