# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem_City(Item):
    prefecture = Field()
    ranking = Field()
    city = Field()
    land_price = Field()
    ping_unit_price = Field()
    change = Field()

class ChainItem_Price(Item):
    prefecture = Field()
    type = Field()
    year = Field()
    land_price = Field()
    ping_unit_price = Field()
    change = Field()