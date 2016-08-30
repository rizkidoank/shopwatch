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
from shopwatch.utils import check_month

class SitemapShopBukalapakSpider(scrapy.Spider):
    name = "sitemap_shop_bukalapak"
    allowed_domains = ["bukalapak.com"]
    #sitemap_urls = (
    start_urls =(
        #'https://www.bukalapak.com/sitemap-user-1.xml',
        'https://www.bukalapak.com/bakulgps',
    )
    # sitemap_rules = [('/p/', 'parse_product')]
    #sitemap_follow = ['(user)-\d*']

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
        username = response.css("div.user-description h5.user__name a::text").extract_first()
        user_feedback = response.css("div.user-description a.user-feedback-summary::text").extract_first()
        join_date = response.css("div.user-meta-join-at::text").extract_first().lower()
        total_subscriber = response.css("div.user-meta-subscribers-total a::text").extract_first()
        user_level = response.css("div.user-description span.user__level::text").extract_first().lower()
        address = response.css("div.user-address::text").extract_first()
        rejection_rate = response.css("div.user-meta-rejection-rate span::text").extract_first()
        num_products = response.css("li.vert-nav-item a::text").extract_first()

        print("username      : "+ repr(username))
        print("url           : "+ repr(response.url))
        print("user_lv       : "+ repr(user_level))
        print("user-address  : "+ repr(address))
        print("join-date     : "+ repr(join_date))
        print("total-subs    : "+ repr(total_subscriber))
        print("user-fb       : "+ repr(user_feedback))
        print("reject-rate   : "+ repr(rejection_rate))
        print("num-products  : "+ repr(num_products))
        print("Test")
