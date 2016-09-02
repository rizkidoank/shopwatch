# -*- coding: utf-8 -*-
import scrapy
import urllib
import json
import re

class ShopwatchTokopediaXmlSpider(scrapy.Spider):
    name = "shopwatch_tokopedia_xml"
    allowed_domains = ["tokopedia.com"]
    start_urls = (
        'https://www.tokopedia.com/diagostore/casing-one-tone-aluminium-glass-battery-cover-xiaomi-redmi-note',
        'https://www.tokopedia.com/diagostore/casing-one-tone-aluminium-glass-battery-cover-xiaomi-redmi-11s',
        'https://www.tokopedia.com/diagostore/case-ipaky-neo-hybrid-softcase-meizu-m2-note',
        'https://www.tokopedia.com/diagostore/case-aluminium-glass-iphone-backcase-hardcase-xiaomi-redmi-note-2',
        'https://www.tokopedia.com/diagostore/casing-two-tone-aluminium-glass-battery-cover-xiaomi-redmi-note',
        'https://www.tokopedia.com/diagostore/case-ipaky-tough-armor-softcase-lenovo-a7000',
    )

    def parse(self, response):
        print(response.url)
        prod_id = response.css("#product-id::attr('value')").extract_first()
        print(prod_id)

        query = urllib.parse.urlencode(dict(p_id=prod_id))
        res = urllib.request.urlopen("https://www.tokopedia.com/ajax/product-review-talk-count.pl?" + query)
        res = res.read().decode("utf-8")
        json_data = json.loads(res)

        talk_count = json_data["talk_count"]
        success = json_data["success"]
        review_count = json_data["review_count"]

        print(talk_count)
        print(success)
        print(review_count)

        query = urllib.parse.urlencode(dict(pid=prod_id,callback='show_product_view'))
        res = urllib.request.urlopen("https://www.tokopedia.com/provi/check?" + query)
        res = res.read().decode("utf-8")
        res = re.sub("^[^(]*|\(|\)","",res)
        json_data = json.loads(res)

        view = json_data["view"]
        print(view)

        query = urllib.parse.urlencode(dict(pid=prod_id, callback='show_product_stats'))
        res = urllib.request.urlopen("https://js.tokopedia.com/productstats/check?" + query)
        res = res.read().decode("utf-8")
        res = re.sub("^[^(]*|\(|\)", "", res)
        json_data = json.loads(res)

        reject = json_data["reject"]
        success = json_data["success"]
        item_sold = json_data["item_sold"]

        print(reject)
        print(success)
        print(item_sold)



