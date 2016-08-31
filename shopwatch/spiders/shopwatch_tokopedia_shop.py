# -*- coding: utf-8 -*-
import scrapy
from  pymongo import MongoClient
from scrapy.spiders import SitemapSpider
from shopwatch.items import Shop
import re
import json

class ShopwatchTokopediaShopSpider(SitemapSpider):
    name = "shopwatch_tokopedia_shop"
    allowed_domains = ["tokopedia.com"]
    sitemap_urls = (
        'https://www.tokopedia.com/sitemaps/shops.xml.gz',
    )
    splash_args = {
        'html': 1,
        'images': 0,
        'png': 0,
        'wait': 5.0
    }

    def __init__(self):
        super(ShopwatchTokopediaShopSpider, self).__init__()
        self.shop = Shop()
        conn = MongoClient(
            host="localhost",
            port=27017
        )
        self.db = conn.shopwatch

    def parse(self, response):
        url = "%s/info" % (response.url)
        yield scrapy.Request(
            url,
            callback=self.parse_info,
        )

    def parse_info(self, response):
        elms = response.css('div.row-fluid.shop-statistics  ul  li div strong::text').extract()
        self.shop['success_transactions'] = int(re.sub("\D*", "", elms[0]))
        self.shop['sold_products'] = int(re.sub("\D*", "", elms[1]))
        self.shop['total_etalase'] = int(re.sub("\D*", "", elms[2]))
        self.shop['total_products'] = int(re.sub("\D*", "", elms[3]))
        self.shop['shop_id'] = str(response.css('#shop-id::attr("value")').extract_first())
        self.shop['owner'] = response.css('div.shop-owner-wrapper h3 a::attr("href")').extract_first()
        self.shop["uri"] = response.url
        self.shop["name"] = response.css('[itemprop="name"]::text').extract_first()
        url_rep = "https://inbox.tokopedia.com/v1/reputation/shop/%s" % (self.shop['shop_id'])
        yield self.shop

    #### NOT YET IMPLEMENTED ####
    def parse_reputation(self, response):
        json_data = json.loads(response.body_as_unicode())
        self.shop['reputations'] = int(re.sub("\D*", "", json_data["data"]["shop_score"]))
        url_fav = "https://js.tokopedia.com/js/shoplogin?id=%s" % (self.shop['shop_id'])
        yield scrapy.Request(
            url=url_fav,
            callback=self.parse_favorit,
        )

    def parse_favorit(self, response):
        res = re.sub("show_last_online|\(|\)", "", response.body_as_unicode())
        json_data = json.loads(res)
        self.shop["favorit"] = int(json_data["FavoriteCount"])
        yield self.shop


