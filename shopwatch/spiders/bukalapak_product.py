# -*- coding: utf-8 -*-
import scrapy, urllib, re, json
from shopwatch.items import Product
from scrapy import Request
from scrapy_splash import SplashRequest
from pymongo import MongoClient
from bs4 import BeautifulSoup

class BukalapakProductSpider(scrapy.Spider):
    name = "bukalapak_product"
    allowed_domains = ["bukalapak.com"]
    start_urls = (
        'http://www.bukalapak.com/',
    )

    splash_args = {
        'html': 1,
        'images': 0,
        'png': 0,
        'wait': 5.0
    }

    def start_requests(self):
        client = MongoClient("localhost", 27017)
        db = client.shopwatch
        self.products = db.products
        owner_url = 'https://www.bukalapak.com/venusshop_ori'
        for prod in self.products.find({'owner_url': owner_url}):
            yield SplashRequest(
                url=prod['url'],
                callback=self.parse,
                endpoint='render.json',
                args=self.splash_args
            )

    def __init__(self):
        self.product = Product()
        self.shop_url = None

    def parse(self, response):
        # Views
        view = int(response.css(".kvp__value[title='Dilihat'] > strong::text").extract_first())

        # Product stats
        if(len(response.css(".kvp__value[title='Terjual'] > strong::text").extract()) > 0):
            item_sold = int(response.css(".kvp__value[title='Terjual'] > strong::text").extract_first())
        else:
            item_sold = 0

        # Product URL
        url = response.url

        # Product name
        name = response.css("[itemprop='name']::text").extract_first()
        name = re.sub("\n", "", name)

        # Product desc
        desc = response.css(".product-detailed-spec div > div >p").extract_first()
        desc = BeautifulSoup(desc, "lxml")
        desc = str.lower(desc.getText())

        # Product image
        img_url = response.css("[itemprop='image']::attr('src')").extract_first()

        # Product price and currency
        price = response.css("[itemprop='price']::attr('content')").extract_first()
        price = re.sub("\D", "", price)
        price = int(price)
        currency = response.css("[itemprop='priceCurrency']::attr('content')").extract_first()

        # Product category
        category = response.css("[itemprop='category']::text").extract_first()
        category = re.sub("\n", "", category)


        # Product owner
        owner_url = self.products.find_one({'url': response.url})['owner_url']

        # Product site
        site = self.products.find_one({'url':response.url})['site']

        self.product['url'] = url
        self.product['name'] = name
        self.product['price'] = price
        self.product['currency'] = currency
        self.product['seen'] = view
        self.product['sold'] = item_sold
        self.product['img_url'] = img_url
        self.product['desc'] = desc
        self.product['owner_url'] = owner_url
        self.product['category'] = category
        self.product['site'] = site


        yield self.product