# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings
from shopwatch.items import Product,Shop

class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]

    def process_item(self, item, spider):
        if (isinstance(item,Shop)):
           self.db.shops.insert(dict(item))
        elif (isinstance(item,Product)):
           if(self.db.products.find({'url':item['url']}).count() > 0):
               self.db.products.update({'url':item['url']},dict(item))
           else:
               self.db.products.insert(dict(item))
        return item
