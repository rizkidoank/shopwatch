# -*- coding: utf-8 -*-
import scrapy


class SitemapShopBukalapakSpider(scrapy.Spider):
    name = "sitemap_shop_bukalapak"
    allowed_domains = ["bukalapak.com"]
    start_urls = (
        'http://www.bukalapak.com/',
    )

    def parse(self, response):
        pass
