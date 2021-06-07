# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


from pymongo import MongoClient
from scrapy import Item


class MongoDBPipeline(object):

    # 打开数据库
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = spider.settings.get('MONOGDB_DB_NAME', 'scrapy_db')

        self.db_client = MongoClient(db_uri)
        self.db = self.db_client[db_name]

    # 关闭数据库
    def close_spider(self, spider):
        self.db_client.close()

    # 对数据进行处理
    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    # 插入数据
    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)
        self.db.books.insert(item)





