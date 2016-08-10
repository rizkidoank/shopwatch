# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from shopwatch.items import Shop,Product

class TokopediaShopSpider(scrapy.Spider):
    name = "tokopedia_shop"
    allowed_domains = ["tokopedia.com"]
    start_urls = (
        'https://www.tokopedia.com/diagostore/info',
    )
    splash_args = {
        'html':1,
        'images':0,
        'png':0,
        'wait':0.5,
    }

    def __init__(self):
        self.shop = Shop()
        self.product = Product()

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse_info,
                endpoint='render.json',
                args=self.splash_args
            )


    def parse_info(self, response):
        elms = response.css('div.row-fluid.shop-statistics  ul  li div strong::text').extract()
        self.shop['success_transactions'] = int(elms[0].replace(".", ""))
        self.shop['sold_products'] = int(elms[1].replace(".", ""))
        self.shop['total_etalase'] = int(elms[2].replace(".", ""))
        self.shop['total_products'] = int(elms[3].replace(".", ""))
        self.shop['shop_id'] = response.css('#shop-id::attr("value")').extract_first()
        self.shop['owner'] = response.css('div.shop-owner-wrapper h3 a::attr("href")').extract_first()
        yield SplashRequest(
                url=response.url.replace("/info",""),
                callback=self.parse_product_lists,
                endpoint='render.json',
                args=self.splash_args)

    def parse_product_lists(self, response):
        elm = response.css('div.pagination.text-right ul li a::attr("href")').extract()
        products = response.css('#showcase-container div.grid-shop-product div.product').extract()
        for product in products:
            self.product = Product()
            res = Selector(text=product)
            self.product["shop_id"] = self.shop["shop_id"]
            self.product["url"] = res.css('div.product a::attr("href")').extract_first()
            self.product["img"] = res.css('div.product-image img::attr("src")').extract_first()
            self.product["name"] = res.css('div.meta-product b::text').extract_first()
            self.product["price"] = res.css('span.price::text').extract_first().replace("Rp ", "").replace(".", "")
            self.product["currency"] = res.css('div.meta-product meta::attr("content")').extract_first()
            yield SplashRequest(
                    url=self.product["url"],
                    callback=self.parse_product,
                    endpoint='render.json',
                    args=self.splash_args)

        if(len(elm) == 1):
            if (response.url.find("page") == -1):
                next_url=elm[0]
                yield SplashRequest(
                    url=next_url,
                    callback=self.parse_product_lists,
                    endpoint='render.json',
                    args=self.splash_args)
            elif (response.url.find("page") > -1):
                yield self.shop
        elif((len(elm) == 2) and (response.url.find("page") != -1 )):
            next_url=elm[1]
            yield SplashRequest(
                url=next_url,
                callback=self.parse_product_lists,
                endpoint='render.json',
                args=self.splash_args)

    def parse_product(self, response):
        detail_info = response.css('div.detail-info dd').extract()
        self.product["sold_count"]=response.css('dd.item-sold-count').extract_first()
        self.product["weight"]= detail_info[1]
        self.product["insurance"]=detail_info[3]
        self.product["condition"]=detail_info[4]
        self.product["min_order"]=detail_info[5]
        yield self.product
