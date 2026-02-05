import scrapy
import json
from scrapy_scrapers.items import Product


class DnslKeSpider(scrapy.Spider):
    name = "dnsl_ke"
    allowed_domains = ["dnsl.co.ke"]
    start_urls = ["https://dnsl.co.ke/?s=Epson&post_type=product&product_cat=0"]
    brand = "Epson"

    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',}

    def parse(self, response):
        json_tags = response.xpath('//span[contains(@class, "gtm4wp_productdata")]')

        self.logger.info(f"Знайдено {len(json_tags)} товарів на сторінці: {response.url}")

        for tag in json_tags:
            json_str = tag.xpath('./@data-gtm4wp_product_data').get()
            if not json_str:
                continue
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError:
                continue

            name = data.get("item_name") or data.get("name") or ""

            if self.brand.lower() not in name.lower():
                continue

            item = Product()
            item["name"] = name
            item["url"] = data.get("productlink")
            item["mpn"] = data.get("sku")
            item["price"] = data.get("price")
            item["stock"] = data.get("stockstatus")
            item["id"] = data.get("internal_id") or data.get("id")

            item["ean"] = data.get("gtin")
            item["average_rating"] = None
            item["description"] = None

            yield item

        next_page = response.xpath("//a[contains(@class, 'next')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)