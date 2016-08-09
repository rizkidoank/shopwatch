# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Shop(scrapy.Item):
    shop_id = scrapy.Field()
    name = scrapy.Field()
    owner = scrapy.Field()
    success_transactions = scrapy.Field()
    sold_products = scrapy.Field()
    total_etalase = scrapy.Field()
    total_products = scrapy.Field()
    products = scrapy.Field()

class Product(scrapy.Item):
    shop_id = scrapy.Field()
    url = scrapy.Field()
    img = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()