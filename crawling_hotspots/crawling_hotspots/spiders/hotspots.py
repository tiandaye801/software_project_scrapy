import scrapy
from ..items import CrawlingHotspotsItem
import string
f = open('../../../page.txt', 'r')
pagein = f.read()
f.close()

class HotspotsSpider(scrapy.Spider):
    name = 'hotspots'
    allowed_domains = ['baidu.com']
    start_urls = ['http://www.baidu.com/']
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    page_limit = pagein       # 用户自行设定查询最大页数
    page = 1
    a_page = ''
    def parse(self, response):
        self.page_limit=int(self.page_limit)
        if (self.page == 1): 
            current_page = response.xpath("/html/body/div[1]/div[3]/div[2]/div/a[1]/@href").extract()
            for i in current_page:
                self.a_page = str(i)
            self.a_page = self.a_page[:-2]
        for counts in range(1+(self.page-1)*10,1+self.page*10):
            detail_url = ''
            item = CrawlingHotspotsItem()
            address = response.xpath("//*[@id={cou}]/div/h3/a/@href".format(cou=counts)).extract()
            # yield scrapy.Request(url=address,callback=self.parse_detail,meta={'item':item})
            item['address'] = address
            for j in address:
                detail_url = str(j)
            if (detail_url == ''): 
                yield item
                self.page = self.page_limit
                break
            else:   
                yield scrapy.Request(url=detail_url,callback=self.parse_detail,meta={'item':item})
        if (self.page < self.page_limit):
            self.page += 1;
            new_page = 'https://www.baidu.com' + self.a_page
            new_page = new_page + '{num}'.format(num=10*(self.page-1))
            yield scrapy.Request(url=new_page,callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        topic = response.xpath("/html/body/div/div/div/div[2]/div[1]/div/h2/text()").extract()
        item['topic'] = topic
        yield item