# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaskItem(scrapy.Item):
    link = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
