import scrapy
from scrapy import Request, Spider
from urllib.parse import quote
from ..items import ScrapyuniversalItem

f = open('../../../links.txt', 'r')
start_url = f.read()
f.close()

f1 = open('../../../num.txt', 'r')
num = f1.read()
f1.close()

class baijiahao(scrapy.Spider):

    name = 'baijiahao'
    start_urls = [start_url]
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


    def parse(self, response):
        for i in range(int(num)): # 可以让前端用户自行输入要查找的条数
            item = ScrapyuniversalItem() 
            comment = response.xpath("/html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[{}]/div/div[2]/div[2]/span/text()".format(i+1)).extract()
            name = response.xpath("/html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[{}]/div/div[2]/div[1]/h5/text()".format(i+1)).extract()
            time = response.xpath("/html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[{}]/div/div[2]/div[3]/div[1]/span[1]/text()".format(i+1)).extract()
            topic = response.xpath("/html/body/div/div/div/div[2]/div[1]/div/h2/text()").extract()
            item['comment'] = comment
            item['time'] = time
            item['topic'] = topic
            item['name'] = name
            yield item