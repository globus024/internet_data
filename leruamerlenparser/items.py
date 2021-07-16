# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def change_photo_link(value):
    value = value.replace(',w_82', ',w_1000').replace(',h_82', ',h_1000')
    return value

def change_article(value):
    value = value.replace('Арт. ', '').replace(' ', '')
    return value

def price_former(value):
    try:
        value = float(value)
        return value
    except ValueError:
        return None

class LeruamerlenparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(change_photo_link))
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_former), output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    article = scrapy.Field(input_processor=MapCompose(change_article), output_processor=TakeFirst())
