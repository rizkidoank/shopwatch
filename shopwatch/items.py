# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Shop(scrapy.Item):
    shop_id = scrapy.Field()
    name = scrapy.Field()
    total_products = scrapy.Field()
    uri = scrapy.Field()

class Product(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    seen = scrapy.Field()
    sold = scrapy.Field()
    reviews = scrapy.Field()
    img_url = scrapy.Field()
    desc = scrapy.Field()
    owner_url = scrapy.Field()
    category = scrapy.Field()
    site = scrapy.Field()
