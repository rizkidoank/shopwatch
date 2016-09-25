# -*- coding: utf-8 -*-
import scrapy, urllib, re, json
from shopwatch.items import Product
from scrapy import Selector
from scrapy_splash import SplashRequest

class TokopediaProductSpider(scrapy.Spider):
    name = "tokopedia_product"
    allowed_domains = ["tokopedia.com"]

    splash_args = {
        'html': 1,
        'images': 0,
        'png': 0,
        'wait': 5.0
    }

    start_urls = (
        'https://www.tokopedia.com/diagostore',
    )

    def __init__(self):
        self.product = Product()
        self.shop_url = None

    def parse(self, response):
        yield SplashRequest(
            url=response.url,
            callback=self.parse_product_lists,
            endpoint='render.json',
            args=self.splash_args
        )

    def parse_product_lists(self, response):
        elm = response.css('div.pagination.text-right ul li a::attr("href")').extract()
        products = response.css('#showcase-container div.grid-shop-product div.product').extract()
        for product in products:
            res = Selector(text=product)
            p = Product()
            url = res.css('div.product a::attr("href")').extract_first()
            yield SplashRequest(
                url=url,
                callback=self.parse_product,
                endpoint='render.json',
                args=self.splash_args)

        if (len(elm) == 1):
            if (response.url.find("page") == -1):
                next_url = elm[0]
                yield SplashRequest(
                    url=next_url,
                    callback=self.parse_product_lists,
                    endpoint='render.json',
                    args=self.splash_args)
            elif (response.url.find("page") > -1):
                pass

        elif ((len(elm) == 2) and (response.url.find("page") != -1)):
            next_url = elm[1]
            yield SplashRequest(
                url=next_url,
                callback=self.parse_product_lists,
                endpoint='render.json',
                args=self.splash_args)

    def parse_product(self, response):
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

        print(url, name, prod_id, view, item_sold, desc)