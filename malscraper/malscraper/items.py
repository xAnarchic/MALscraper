# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MalscraperItem(scrapy.Item):
    # define the fields for your item here like:
    pass



class MalItem(scrapy.Item):
    jp_title = scrapy.Field()
    eng_title = scrapy.Field()
    show_type = scrapy.Field()
    episode_num = scrapy.Field()
    score = scrapy.Field()
    ranking = scrapy.Field()
    popularity = scrapy.Field()
    studio = scrapy.Field()
    genres_themes = scrapy.Field()
    genres = scrapy.Field()
    themes = scrapy.Field()
    demographics = scrapy.Field()
    synopsis = scrapy.Field()
    link = scrapy.Field()
    episode = scrapy.Field()

class Mal1Item(scrapy.Item):
    episode = scrapy.Field()
    episode_title = scrapy.Field()
    episode_date_aired = scrapy.Field()
    episode_score = scrapy.Field()
    jp_title = scrapy.Field()


