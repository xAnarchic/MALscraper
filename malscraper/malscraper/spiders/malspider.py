# Spider
from typing import Iterable
from urllib.parse import urlencode
import scrapy
import sys
import re
from malscraper.items import MalItem, MalscraperItem
from scrapy import Request
import time


class MALSpider(scrapy.Spider):
    name = 'malspider'
    allowed_domains = ['myanimelist.net', 'proxy.scrapeops.io']
    start_urls = ['https://myanimelist.net/topanime.php?limit=150']   # orders all anime on the website by score

    def parse(self, response):
        animes = response.css('tr.ranking-list')    # returns a list of the 50 anime found on each page
        for anime in animes:  # iterating through each anime to get information
            relative_url = anime.css('h3.fl-l.fs14.fw-b.anime_ranking_h3 a::attr(href)').get()
            yield response.follow(url = relative_url, callback=self.parse_anime, dont_filter = True)

        next_page = response.css('div.di-b.ac.pt16.pb16.pagination.icon-top-ranking-page-bottom a::attr(href)').getall()[-1]  # specifically gets the link to the next page of anime, avoids the "prev page" link
        next_page_url = 'https://myanimelist.net/topanime.php' + next_page

        if next_page != '?limit=300':
            yield response.follow(url = next_page_url, callback = self.parse)
        else:
            print('All pages scraped. Script will now be terminated')
            sys.exit


    def parse_anime(self, response):

        info = response.css('div.spaceit_pad::text').getall()   # list of info about anime
        mal_item = MalItem()


        for item in info:   # iterating over different bits of information within the list
            if re.search('^\n..[0-9]+\n', item) != None:   # locates the episode info using the pattern it presents with
                episode_num = item.strip()  # after removing the whitespaces from the episode info, the 'episode' variable is assigned the episode number
                break   # only looks for the first instance of the pattern before closing the loop
            else:
                episode_num = 'Unknown/ Still airing'   # if the pattern is not found then the anime has yet to finish



        mal_item['jp_title'] = response.css('h1.title-name.h1_bold_none strong::text').get(),
        mal_item['eng_title'] = response.css('p.title-english.title-inherit::text').get(),
        mal_item['show_type'] = response.css('div.spaceit_pad a::text').getall()[0],
        mal_item['episode_num'] =  episode_num

        yield mal_item

if __name__ == '__main__':
    pass


