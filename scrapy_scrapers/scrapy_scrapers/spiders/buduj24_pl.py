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

        name = self.cleanup_string(response.xpath("//h1/span/text()").extract_first())

        if not name or self.brand.lower() not in name.lower():
            return

        item = Product()
        item["url"] = response.url
        item["name"] = name

        item["mpn"] = self.cleanup_string(response.xpath("//span[@class='mpn']/text()").extract_first())
        item["ean"] = self.cleanup_string(response.xpath("//span[@class='ean']/text()").extract_first())
        item["price"] = self.cleanup_string(response.xpath("//span[contains(@class, 'price')]/text()").extract_first())
        item["stock"] = self.cleanup_string(response.xpath("//span[contains(@class, 'availability')]/text()").extract_first())
        item["description"] = self.cleanup_string(response.xpath("//div[@class='product-description']//text()").extract_first())
        item["average_rating"] = self.cleanup_string(response.xpath("//*[contains(@class,'rating-value')]/text()").extract_first())
        item["reviews_amount"] = self.cleanup_string(response.xpath("//*[contains(@class,'review-count')]/text()").extract_first())

        item["id"] = response.url.split("/") [-1]

        yield item

    @staticmethod
    def cleanup_string(value):
         if value:
             return value.strip()
         return None