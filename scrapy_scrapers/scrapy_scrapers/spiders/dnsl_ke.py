import scrapy
from scrapy_scrapers.items import Product

class DnslKeSpider(scrapy.Spider):
    name = "dnsl_ke"
    allowed_domains = ["dnsl.co.ke"]
    start_urls = ["https://dnsl.co.ke/?s=Epson&post_type=product&product_cat=0"]
    brand = "Epson"

    def parse(self, response):
        product_links = response.xpath("//a[contains(@class, 'woocommerce-loop-product__link')]/@href").extract()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

        next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        name = self.clean(response.xpath("//h1/text()").get())

        if not name or self.brand.lower() not in name.lower():
            return

        item = Product()
        item["url"] = response.url
        item["name"] = name
        item["mpn"] = self.cleanup_string(response.xpath("//span[@class='sku']/text()").get())
        item["ean"] = None
        item["price"] = self.cleanup_string("".join(response.xpath("//p[@class='price']//text()").getall()))
        item["stock"] = None
        item["description"] = self.cleanup_string(
            " ".join(response.xpath("//div[@id='tab-description']//text()").getall()))
        item["average_rating"] = self.cleanup_string(
            response.xpath("//div[contains(@class,'star-rating')]/@aria-label").get())
        item["reviews_amount"] = None
        item["id"] = response.url.rstrip("/").split("/")[-1]

        yield item

    def clean(self, value):
        if not value:
            return None
        return " ".join(value.split()).strip()

    @staticmethod
    def cleanup_string(value):
        if value:
            return value.strip()
        return None