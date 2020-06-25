# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlaneticketItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    airRecId = scrapy.Field()
    airCompany = scrapy.Field()
    airFlightNumber = scrapy.Field()
    airCraftModel = scrapy.Field()
    airCraftSize = scrapy.Field()
    airDepartureTime = scrapy.Field()
    airArrivalTime = scrapy.Field()
    airDepartureCity = scrapy.Field()
    airArrivalCity = scrapy.Field()
    airDeparturePort = scrapy.Field()
    airArrivalPort = scrapy.Field()
    airMealType = scrapy.Field()
    airOilFee = scrapy.Field()
    airTax = scrapy.Field()
    airStopTime = scrapy.Field()
    airPrice = scrapy.Field()
    airCabinType = scrapy.Field()
    airOnTimeRate = scrapy.Field()
    airSource = scrapy.Field()
