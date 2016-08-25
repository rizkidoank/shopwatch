# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from shopwatch.items import Shop,Product
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pymongo
from scrapy import settings
from scrapy.spiders import SitemapSpider

class SitemapShopBukalapakSpider(SitemapSpider):
    name = "sitemap_shop_bukalapak"
    allowed_domains = ["bukalapak.com"]
    sitemap_urls = (
        'http://www.bukalapak.com/sitemap.xml',
    )

    # sitemap_follow = ['']
    splash_args = {
        'html': 1,
        'images': 0,
        'png': 0,
        'wait': 5.0
    }

    def __init__(self):
        super(SitemapShopBukalapakSpider, self).__init__()
        self.shop = Shop()
        self.product = Product()
        conn = pymongo.MongoClient(
            host="localhost",
            port=27017
        )
        self.db = conn.shopwatch

    def parse(self, response):
        print(response.url)
        # yield SplashRequest(
        #     url=response.url,
        #     callback=self.parse_product_lists,
        #     endpoint='render.json',
        #     args=self.splash_args
        # )