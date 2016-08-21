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


class SitemapShopTokopediaSpider(SitemapSpider):
    name = "sitemap_shop_tokopedia"
    allowed_domains = ["tokopedia.com"]
    sitemap_urls = (
        'https://www.tokopedia.com/sitemaps/shops.xml.gz',
    )
    splash_args = {
        'html':1,
        'images':0,
        'png':0,
        'wait':5.0
    }

    def __init__(self):
        super(SitemapShopTokopediaSpider, self).__init__()
        self.shop = Shop()
        self.product = Product()
        conn = pymongo.MongoClient(
            host="localhost",
            port=27017
        )
        self.db = conn.shopwatch

    def parse(self, response):
        yield SplashRequest(
            url=response.url,
            callback=self.parse_product_lists,
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
        yield self.shop
        # yield SplashRequest(
        #         url=response.url.replace("/info",""),
        #         callback=self.parse_product_lists,
        #         endpoint='render.json',
        #         args=self.splash_args)

    def parse_product_lists(self, response):
        elm = response.css('div.pagination.text-right ul li a::attr("href")').extract()
        products = response.css('#showcase-container div.grid-shop-product div.product').extract()
        for product in products:
            res = Selector(text=product)
            p = Product()
            url = res.css('div.product a::attr("href")').extract_first()
            yield SplashRequest(
                    url=url ,
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
                pass

        elif((len(elm) == 2) and (response.url.find("page") != -1 )):
            next_url=elm[1]
            yield SplashRequest(
                url=next_url,
                callback=self.parse_product_lists,
                endpoint='render.json',
                args=self.splash_args)

    def parse_product(self, response):
        last_updated = re.split(' |,',response.css("small.product-pricelastupdated i::text").extract_first())
        self.product["last_updated"] = last_updated[3] + " " + last_updated[5]
        self.product["prod_id"] = response.css('#product-id::attr("value")').extract_first()
        if ( self.db.products.find({"prod_id": self.product["prod_id"]}).count()):
            print("Doc exists, update")
            db_last_updated = self.db.products.find_one({"prod_id": self.product["prod_id"]})["last_updated"]
            #if (datetime.strptime(self.product["last_updated"], '%d-%m-%Y %H:%M') > datetime.strptime(db_last_updated, '%d-%m-%Y %H:%M')):
            #    print("Newer pages, replacing old one")
            self.product["url"] = response.url
            self.product["img"] = response.css('div.product-imagebig img::attr("src")').extract_first()
            self.product["name"] = response.css('#breadcrumb-container  li.active  h2::text').extract_first()
            self.product["price"] = int((response.css('div.product-pricetag span[itemprop="price"]::text').extract_first().replace(".", "")))
            self.product["currency"] = response.css('div.product-pricetag span[itemprop="priceCurrency"]::attr("content")').extract_first()
            detail_info = response.css('div.detail-info dd').extract()
            self.product["sold_count"] = response.css('dd.item-sold-count::text').extract_first()
            self.product["weight"] = BeautifulSoup(detail_info[1], 'lxml').getText()
            self.product["insurance"] = BeautifulSoup(detail_info[3], 'lxml').getText()
            self.product["condition"] = BeautifulSoup(detail_info[4], 'lxml').getText()
            self.product["min_order"] = int(BeautifulSoup(detail_info[5], 'lxml').getText())
            self.product['shop_id'] = response.css('#shop-id::attr("value")').extract_first()
            self.db.products.replace_one({"prod_id": self.product["prod_id"]},self.product)
        else:
            print("New doc, insert")
            self.product["url"] = response.url
            self.product["img"] = response.css('div.product-imagebig img::attr("src")').extract_first()
            self.product["name"] = response.css('#breadcrumb-container  li.active  h2::text').extract_first()
            self.product["price"] = int((response.css('div.product-pricetag span[itemprop="price"]::text').extract_first().replace(".", "")))
            self.product["currency"] = response.css('div.product-pricetag span[itemprop="priceCurrency"]::attr("content")').extract_first()
            detail_info = response.css('div.detail-info dd').extract()
            self.product["sold_count"] = response.css('dd.item-sold-count::text').extract_first()
            self.product["weight"] = BeautifulSoup(detail_info[1], 'lxml').getText()
            self.product["insurance"] = BeautifulSoup(detail_info[3], 'lxml').getText()
            self.product["condition"] = BeautifulSoup(detail_info[4], 'lxml').getText()
            self.product["min_order"] = int(BeautifulSoup(detail_info[5], 'lxml').getText())
            self.product["shop_id"] = response.css('#shop-id::attr("value")').extract_first()
            self.product["num-revs"] = response.css('#p-nav-review span::text').extract_first()
            self.product["num-discs"] = response.css('#p-nav-talk span::text').extract_first()
            self.product["desc"] = response.css('p[itemprop = "description"]::text').extract_first()
            yield self.product


