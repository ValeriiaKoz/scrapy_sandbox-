import scrapy
from scrapy_scrapers.items import Product

class Buduj24PLSpider(scrapy.Spider):
    name = "buduj24_pl"
    start_urls = ["https://buduj24.pl/hg-polska/page:1"]
    brand = "hg"

    def parse(self, response):
        product_links = response.xpath("//a[contains(@class, 'product-hover-opacity')]/@href").extract()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

        next_page = response.xpath("//a[contains(@class, 'next')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):

        name = response.xpath("//h1/span/text()").extract_first()
        if name:
            name = name.strip()

        item = Product()
        item["url"] = response.url
        item["name"] = name

        item["mpn"] = response.xpath("//span[@class='mpn']/text()").extract_first()
        if item["mpn"]:
            item["mpn"] = item["mpn"].strip()

        item["ean"] = response.xpath("//span[@class='ean']/text()").extract_first()
        if item["ean"]:
            item["ean"] = item["ean"].strip()

        item["price"] = response.xpath("//span[contains(@class, 'price')]/text()").extract_first()
        if item["price"]:
            item["price"] = item["price"].strip()

        item["stock"] = response.xpath("//span[contains(@class, 'availability')]/text()").extract_first()
        if item["stock"]:
            item["stock"] = item["stock"].strip()

        item["description"] = response.xpath("//div[@class='product-description']//text()").extract_first()

        item["average_rating"] = response.xpath("//*[contains(@class,'rating-value')]/text()").extract_first()
        if item["average_rating"]:
            item["average_rating"] = item["average_rating"].strip()

        item["reviews_amount"] = response.xpath("//*[contains(@class,'review-count')]/text()").extract_first()
        if item["reviews_amount"]:
            item["reviews_amount"] = item["reviews_amount"].strip()

        item["id"] = response.url.split("/") [-1]

        if self.brand.lower() not in (item["name"] or "").lower():
            return

        yield item