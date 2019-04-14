# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .send_email import send_email
from scrapy.exceptions import DropItem
import pymongo
from scrapy.item import Item

class DropDuplicate(object):
    def __init__(self):
        self.question_set = set()
    
    def process_item(self, item, spider):
        question = item['questions']
        if question in self.question_set:
            #舍去重复项
            raise DropItem("Duplicate question found: %s" % question)
        self.question_set.add(question)
        return item

class SuperpowerPipeline(object):
    def process_item(self, item, spider):
        with open("D:/stackoverflow.txt",'a', encoding = 'utf-8') as f:
            f.write('问题:' + item['questions']+ "   票数:" + item['votes'] + "\n")
            f.write("-----------------------\n")
        return item

#使用pymongo连接MongoDB
class MongoPipeLine(object):
    DB_URI = 'mongodb://localhost:27017/'
    DB_NAME = 'test_database'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URI)
        self.db = self.client[self.DB_NAME]
    
    def close_spider(self, spider):
        self.client.close()
    
    def process_item(self, item, spider):
        collection = self.db[spider.name]
        post = dict(item) 
        collection.insert_one(post)
        return item


    

