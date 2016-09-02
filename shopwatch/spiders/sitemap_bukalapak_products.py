# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from datetime import datetime
import urllib

class SitemapBukalapakProductsSpider(scrapy.Spider):
    name = "sitemap_bukalapak_products"
    allowed_domains = ["bukalapak.com"]
    start_urls = (
        'https://www.bukalapak.com/p/motor-471/outwear-motor/masker-slayer/3vcmm-jual-promo-masker-supermask-masker-multi-fungsi-dengan-filter-terstandart-eropa-en149',
    )
    splash_args = {
        'html': 1,
        'images': 0,
        'png': 0,
        'wait': 5.0
    }
    def parse(self, response):
        yield SplashRequest(
            url=response.url,
            callback=self.parse_product,
            endpoint='render.json',
            args=self.splash_args
        )

    def parse_product(self, response):
        name = response.css("[itemprop='name']::text").extract_first()
        name = re.sub("\n","",name)

        price = response.css("[itemprop='price']::attr('content')").extract_first()
        price = re.sub("\D","",price)

        currency = response.css("[itemprop='priceCurrency']::attr('content')").extract_first()

        prod_spec = response.css(".product-spec dd").extract()

        category = response.css("[itemprop='category']::text").extract_first()
        category = re.sub("\n","",category)

        condition = response.css(".product-spec .product__condition::text").extract_first()

        weight = response.css(".product-spec  dd:nth-child(6)::text").extract_first()
        weight = re.sub("\n","",weight)
        weight = re.split("\s",weight)

        weight_val = weight[0]
        weight_unit = str.lower(weight[1])

        ratingCount = response.css("[itemprop='ratingCount']::text").extract_first()
        desc = response.css(".product-detailed-spec div > div >p").extract_first()
        desc = BeautifulSoup(desc,"lxml")
        desc = str.lower(desc.getText())

        stats_entry = response.css(".kvp__value > strong::text").extract()
        peminat = stats_entry[0]
        dilihat = stats_entry[1]

        url = "https://www.bukalapak.com/%s" % (response.css(".product-detailed-manage::attr('data-insert-inside-url')").extract_first())
        res = urllib.request.urlopen(url)
        res = res.read().decode("utf-8")
        last_update = BeautifulSoup(res,"lxml")
        last_update = last_update.find("time").getText()
        last_update = datetime.strptime(last_update,"%Y-%m-%d %H:%M:%S")

        # Required to convert from Human-readable to datetime
        # last_update = str.lower(stats_entry[2])
        # today = re.compile("hari ini")
        # if(today.match(last_update)):
        #     last_update = datetime.date.today()

        terjual = stats_entry[4]

        print(name)
        print(price)
        print(currency)
        print(category)
        print(condition)
        print(weight_val)
        print(weight_unit)
        print(ratingCount)
        print(desc)
        print(peminat)
        print(dilihat)
        print(last_update)
        print(terjual)
