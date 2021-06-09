
import jieba
from pymongo import MongoClient
from jieba import analyse
import os

# https://pypi.org/project/pymongo/
# http://github.com/mongodb/mongo-python-driver
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from collections import Counter
from imageio import imread
from matplotlib.font_manager import FontProperties


def get_words_frequency(collection, stop_set):
    array = collection.find({}, {"_id": 0, "comment": 1})
    num = 0
    words_list = []
    for doc in array:
        num += 1
        # print(doc['comments'])
        comments = doc['comment']
        t_list = jieba.lcut(str(comments), cut_all=False)
        for word in t_list:
            if word not in stop_set and 5 > len(word) > 1:
                words_list.append(word)
        words_dict = dict(Counter(words_list))

    return words_dict


def classify_frequency(word_dict, minment=5):
    num = minment - 1
    dict = {k: v for k, v in word_dict.items() if v > num}
    return dict


def load_stopwords_set(stopwords_path):
    stop_set = set()
    with open(str(stopwords_path), 'r', encoding='UTF-8') as fp:
        line = fp.readline()
        while line is not None and line != "":
            # print(line.strip())
            stop_set.add(line.strip())
            line = fp.readline()
            # time.sleep(2)
    return stop_set


def get_wordcloud(dict, title, save=False):
    # 词云设置
    mask_color_path = "./static/images/bg_1.png"  # 设置背景图片路径
    font_path = './static/fonts/FZXingKai-S04S.TTF'  # 为matplotlib设置中文字体路径没
    imgname2 = "./static/images/color_by_img.png"  # 保存的图片名字2(颜色按照背景图片颜色布局生成)
    width = 1000
    height = 860
    margin = 2
    # 设置背景图片
    mask_coloring = imread(mask_color_path)
    # 设置WordCloud属性
    wc = WordCloud(font_path=font_path,  # 设置字体
                   background_color="white",  # 背景颜色
                   max_words=150,  # 词云显示的最大词数
                   mask=mask_coloring,  # 设置背景图片
                   max_font_size=200,  # 字体最大值
                   # random_state=42,
                   width=width, height=height, margin=margin,  # 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                   )
    # 生成词云
    wc.generate_from_frequencies(dict)

    bg_color = ImageColorGenerator(mask_coloring)
    # 重定义字体颜色
    wc.recolor(color_func=bg_color)
    # 定义自定义字体，文件名从1.b查看系统中文字体中来
    myfont = FontProperties(fname=font_path)
    plt.figure()
    plt.title(title, fontproperties=myfont)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

    if save is True:  # 保存到
        wc.to_file(imgname2)


if __name__ == '__main__':
    os.chdir = '../../'
    stopwords_path = './static/stopwords/stopwords.txt'
    stop_set = load_stopwords_set(stopwords_path)

    # 数据库连接
    client = MongoClient('localhost', 27017)
    db = client.scrapy_db
    collection = db.books

    # # print(Headers.getUA())
    try:
        # 从数据库获取评论 并分好词
        frequency_dict = get_words_frequency(collection, stop_set)
        # 对词频进一步筛选
        cl_dict = classify_frequency(frequency_dict, 5)
        # print(frequency_dict)
        # 根据词频 生成词云
        get_wordcloud(cl_dict, "词云")
    finally:
        # pass
        client.close()
