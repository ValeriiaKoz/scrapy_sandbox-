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

        next_page = response.xpath("a.next::attr(href)").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):

        name = response.xpath("//h1/span/text()").extract_first()
        mpn = response.xpath("//span[@class='mpn']/text()").extract_first()
        ean = response.xpath("//span[@class='ean']/text()").extract_first()
        price = response.xpath("//span[contains(@class, 'price')]/text()").extract_first()
        stock = response.xpath("//span[contains(@class, 'availability')]/text()").extract_first()
        description = response.xpath("//div[@class='product-description']//text()").extract_first()
        average_rating = response.xpath("//*[contains(@class,'rating-value')]/text()").extract_first()
        reviews_amount = response.xpath("//*[contains(@class,'review-count')]/text()").extract_first()

        if self.brand.lower() not in name.lower():
            return

        item = Product()
        item["url"] = response.url
        item["name"] = name
        item["mpn"] = mpn
        item["ean"] = ean
        item["price"] = price
        item["stock"] = stock
        item["description"] = description
        item["average_rating"] = average_rating
        item["reviews_amount"] = reviews_amount
        item["id"] = response.url.split("/") [-1]

        yield item