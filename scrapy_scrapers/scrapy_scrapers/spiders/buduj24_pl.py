import scrapy
from scrapy_scrapers.items import Product

class Buduj24PLSpider(scrapy.Spider):
    name = "buduj24_pl"
    allowed_domains =["buduj24.pl"]
    start_urls = ["https://buduj24.pl/hg-polska/page:1"]
    brand = "hg"

    def parse(self, response):
        product_links = response.css(".product-hover-opacity a::attr(href)").getall()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

        next_page = response.css("a.next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):

        name = response.css("h1 span::text").get()
        print(name)
        mpn = response.css("span.mpn::text").get()
        print(mpn)
        ean = response.css("span.ean::text").get()
        print(ean)
        price = response.css("span.price::text").get()
        print(price)
        stock = response.css("span.availability::text").get()
        print(stock)
        description = response.css("div.product-description").get()
        print(description)
        rating = response.css(".rating-value::text").get()
        print(rating)
        reviews = response.css(".review-count::text").get()
        print(reviews)

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