# -*- coding: utf-8 -*-
import scrapy, urllib, re, json
from shopwatch.items import Product
from scrapy import Selector
from scrapy_splash import SplashRequest


class TokopediaProductsListSpider(scrapy.Spider):
    name = "tokopedia_products_list"
    allowed_domains = ["tokopedia.com"]

    splash_args = {
        'html': 1,
        'images': 0,
        'png': 0,
        'wait': 5.0
    }

    start_urls = (
        'https://www.tokopedia.com/mitrakamera',
    )

    def __init__(self):
        self.product = Product()
        self.shop_url = None

    def parse(self, response):
        self.shop_url = response.url
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
            self.product['url'] = url
            self.product['owner_url'] = self.shop_url
            self.product['site'] = 'tokopedia'
            yield self.product

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