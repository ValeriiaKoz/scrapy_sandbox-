import scrapy
from scrapy_scrapers.items import Product

class Buduj24PLSpider(scrapy.Spider):
    name = "buduj24_pl"
    allowed_domains =["buduj24.pl"]
    start_urls = ["https://buduj24.pl/hg-polska/page:1"]
    brand = "hg-polska"

    def parse(self, response):
        product_links = response.css("a.product-link::attr(href)").getall()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

        next_page = response.css("a.next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):

        name = response.css("h1.title::text").get()
        mpn = respnse.css("span.mpn::text").get()
        ean = response.css("span.ean::text").get()
        price = response.css("span.price::text").get()
        stock = response.css("span.stock::text").get()
        description = response.css("#description::text").get()
        rating = response.css(".rating-value::text").get()
        reviews = response.css(".review-count::text").get()

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
        item["rating"] = rating
        item["reviews"] = reviews
        item["id"] = response.url.split("/") [-1]

        yield item