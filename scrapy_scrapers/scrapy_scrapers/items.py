
import scrapy


class Product(scrapy.Item):
    id = scrapy.Field()
    mpn = scrapy.Field()
    ean = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    average_rating = scrapy.Field()
    reviews_amount = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()

