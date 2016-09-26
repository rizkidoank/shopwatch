# -*- coding: utf-8 -*-
import scrapy, urllib, re, json
from shopwatch.items import Product
from scrapy import Selector,Request
from scrapy_splash import SplashRequest
from pymongo import MongoClient

class TokopediaProductSpider(scrapy.Spider):
    name = "tokopedia_product"
    allowed_domains = ["tokopedia.com"]

    def start_requests(self):
        client = MongoClient("localhost",27017)
        db = client.shopwatch
        products = db.products
        owner_url = 'https://www.tokopedia.com/bakulgps'
        for prod in products.find({'owner_url':owner_url}):
            yield Request(prod['url'])

    def __init__(self):
        self.product = Product()
        self.shop_url = None

    def parse(self, response):
        # Product ID
        prod_id = response.css("#product-id::attr('value')").extract_first()

        # Views
        query = urllib.parse.urlencode(dict(pid=prod_id, callback='show_product_view'))
        res = urllib.request.urlopen("https://www.tokopedia.com/provi/check?" + query)
        res = res.read().decode("utf-8")
        res = re.sub("^[^(]*|\(|\)", "", res)
        json_data = json.loads(res)
        view = json_data["view"]

        # Product stats
        query = urllib.parse.urlencode(dict(pid=prod_id, callback='show_product_stats'))
        res = urllib.request.urlopen("https://js.tokopedia.com/productstats/check?" + query)
        res = res.read().decode("utf-8")
        res = re.sub("^[^(]*|\(|\)", "", res)
        json_data = json.loads(res)
        item_sold = json_data["item_sold"]

        # Product URL
        url = response.url

        # Product name
        name = response.css('[itemprop="name"]::text').extract_first()

        # Product desc
        desc = response.css('p[itemprop = "description"]::text').extract()
        desc = str.lower((' ').join(desc))

        # Product image
        img_url = response.css("img[itemprop='image']::attr('src')").extract_first()

        # Product owner
        owner_url = response.css("a#shop-name-info::attr('href')").extract_first()

        #Product price
        price = int((response.css('div.product-pricetag span[itemprop="price"]::text').extract_first().replace(".", "")))

        # Product category
        category = response.css("ul[itemprop='breadcrumb'] > li > h2 > a::text").extract()
        category = category[len(category)-1]


        self.product['url'] = url
        self.product['name'] = name
        self.product['price'] = price
        self.product['currency'] = 'IDR'
        self.product['seen'] = view
        self.product['sold'] = item_sold
        self.product['img_url'] = img_url
        self.product['desc'] = desc
        self.product['owner_url'] = owner_url
        self.product['category'] = category
        self.product['site'] = 'tokopedia'

        yield self.product