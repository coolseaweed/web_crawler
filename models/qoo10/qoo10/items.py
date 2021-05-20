# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Qoo10Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()
    Category = scrapy.Field()
    Question = scrapy.Field()
    Answer = scrapy.Field()
    URL = scrapy.Field()
    # Price       = scrapy.Field()
    # Features    = scrapy.Field()
    # Description = scrapy.Field()
    # SpecsName   = scrapy.Field()
    # Specs       = scrapy.Field()


