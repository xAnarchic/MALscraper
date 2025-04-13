# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MalscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MalItem(scrapy.Item):
    jp_title = scrapy.Field()
    eng_title = scrapy.Field()
    show_type = scrapy.Field()
    episode_num = scrapy.Field()

