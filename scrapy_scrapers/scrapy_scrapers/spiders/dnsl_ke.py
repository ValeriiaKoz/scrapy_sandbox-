import scrapy
from scrapy_scrapers.items import Product

class DnslKeSpider(scrapy.Spider):
    name = "dnsl_ke"
    start_urls = ["https://dnsl.co.ke/?s=Epson&post_type=product&product_cat=0"]
    brand = "Epson"

    def parse(self, response):
        product_links = response.xpath("//h2[@class='woocommerce-loop-product__title']/a/@href").extract()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

        next_page = response.xpath("//a[@class='next page-numbers']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        name = self.cleanup_string(response.xpath("//h1/text()").extract_first())

        if not name or self.brand.lower() not in name.lower():
            return

        item = Product()
        item["url"] = response.url
        item["name"] = name

        item["mpn"] = self.cleanup_string(response.xpath("//span[@class='sku']/text()").extract_first())
        item["ean"] = None
        item["price"] = self.cleanup_string(response.xpath("//p[@class='price']//text()").extract_first())
        item["stock"] = None
        item["description"] = self.cleanup_string(response.xpath("//div[@id='tab-description']//text()").extract_first())
        item["average_rating"] = self.clean_string(response.xpath("//div[contains(@class,'star-rating')]/@aria-label").extract_first())
        item["reviews_amount"] = None
        item["id"] = response.url.split("/")[-1]
        yield item

@staticmethod
def cleanup_string(value):
    if value:
        return value.strip()
    return None