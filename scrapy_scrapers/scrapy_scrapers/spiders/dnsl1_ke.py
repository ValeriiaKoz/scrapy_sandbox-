import scrapy
from scrapy_scrapers.items import Product

class Dnsl1KeSpider(scrapy.Spider):
    name = "dnsl1_ke"
    start_urls = ["https://dnsl.co.ke/?s=Epson&post_type=product&product_cat=0"]
    brand = "Epson"

    def parse(self, response):
        product_links = response.xpath("//h2[@class='woocommerce-loop-product__title']/a/@href").getall()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

        next_page  = response.xpath("//a[@class='next page-numbers']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        name = self.cleanup_string(response.xpath("//h1/text()").get())

        if not name or self.brand.lower() not in name.lower():
            return

        item = Product(
            url=response.url,
            name=name,
            mpn=self.cleanup_strin(response.xpath("//span[@class='sku']/text()").get()),
            ean=None,
            price=self.cleanup_string(response.xpath("//p[@class='price']//text()").get()),
            stock=None,
            description=self.cleanup_string(response.xpath("//div[@id='tab-description']//text()").get()),
            average_rating=self.cleanup_string(response.xpath("//div[contains(@class,'star-rating')]/@aria-label").get()),
            reviews_amount=None,
            id=response.url.split("/")[-1])
        yield item

    @staticmethod
    def cleanup_string(value):
        return value.strip() if value else None