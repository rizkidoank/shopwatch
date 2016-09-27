# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy import Request, Selector
from shopwatch.items import Product


class BukalapakProductsListSpider(scrapy.Spider):
    name = "bukalapak_products_list"
    allowed_domains = ["bukalapak.com"]

    splash_args = {
        'html': 1,
        'images': 0,
        'png': 0,
        'wait': 5.0
    }

    start_urls = (
        'https://www.bukalapak.com/venusshop_ori/products',
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
        elm = response.css('a.next_page::attr("href")').extract()
        products = response.css("div.product-media a::attr('href')").extract()
        self.shop_url = str(response.url).replace('/products','').split('?')[0]
        for product in products:
            prod_url = str(product).replace('?from=list-product','')
            p = Product()
            self.product['url'] = prod_url
            self.product['owner_url'] = self.shop_url
            if 'tokopedia' in response.url:
                self.product['site'] = 'tokopedia'
            elif 'bukalapak' in response.url:
                self.product['site'] = 'bukalapak'
            yield self.product

            if (len(elm) == 1):
                str_url = str(elm[0]).split('&')[0]
                next_url = 'https://www.bukalapak.com'+str_url
                yield SplashRequest(
                    url=next_url,
                    callback=self.parse_product_lists,
                    endpoint='render.json',
                    args=self.splash_args)