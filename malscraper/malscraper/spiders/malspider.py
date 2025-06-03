# Spider
from typing import Iterable

import scrapy
import sys
import re
from malscraper.items import MalItem, Mal1Item
import time
from scrapy import signals

from scrapy import Request


class MALSpider(scrapy.Spider):
    name = 'malspider'
    item_count = 0
    allowed_domains = ['myanimelist.net', 'proxy.scrapeops.io']
    start_urls = ['https://myanimelist.net/topanime.php']   # orders all anime on the website by score

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MALSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        spider.crawler = crawler
        return spider

    def item_scraped(self, item):
        self.item_count += 1
        if self.item_count % 30 == 0:
            self.logger.info(f'Pausing job... scrape count is currently: {self.item_count}')
            self.crawler.engine.pause()
            time.sleep(30)
            self.crawler.engine.unpause()
            self.logger.info('Resuming job... :)')


    def parse(self, response):

        animes = response.css('tr.ranking-list')    # returns a list of the 50 anime found on each page

        for anime in animes:  # iterating through each anime to get information
            relative_url = anime.css('h3.fl-l.fs14.fw-b.anime_ranking_h3 a::attr(href)').get()
            yield response.follow(url = relative_url, callback=self.parse_anime, dont_filter = True)

        next_page = response.css('div.di-b.ac.pt16.pb16.pagination.icon-top-ranking-page-bottom a::attr(href)').getall()[-1]  # specifically gets the link to the next page of anime, avoids the "prev page" link
        next_page_url = 'https://myanimelist.net/topanime.php' + next_page


        if next_page != '?limit=1000':
            yield response.follow(url = next_page_url, callback = self.parse)
        elif self.item_count == 3000:
            sys.exit()




    def parse_anime(self, response):

        mal_item = MalItem()

        info = response.css('div.spaceit_pad::text').getall()   # list of info about anime

        for item in info:   # iterating over different bits of information within the list
            if re.search('^\n..[0-9]+\n', item) is not None:   # locates the episode info using the pattern it presents with
                episode_num = item.strip()  # after removing the whitespaces from the episode info, the 'episode' variable is assigned the episode number
                break   # only looks for the first instance of the pattern before closing the loop
            else:
                episode_num = 'Unknown/ Still airing'   # if the pattern is not found then the anime has yet to finish


        episode_info_url = response.css('div[id=horiznav_nav] a::attr(href)').getall()[2]
        if episode_info_url[-7:] == 'episode':
            yield response.follow(url = episode_info_url, callback = self.episode_parse)
        else:
            link = response.css('div.di-ib a::attr(href)').getall()[-2]
            yield response.follow(url = link, callback = self.lone_episode_parse)


        mal_item['jp_title'] = response.css('h1.title-name.h1_bold_none strong::text').get(),
        mal_item['eng_title'] = response.css('p.title-english.title-inherit::text').get(),
        mal_item['show_type'] = response.css('div.spaceit_pad a::text').getall()[0],
        mal_item['episode_num'] =  episode_num
        mal_item['score'] = response.css('div.fl-l.score div::text').get()
        mal_item['ranking'] = response.css('span.numbers.ranked strong::text').get()[1:]
        mal_item['popularity'] = response.css('span.numbers.popularity strong::text').get()[1:]
        mal_item['studio'] = response.css('span.information.studio.author a::text').get()
        mal_item['genres_themes'] = response.css('span[itemprop=genre]::text').getall()
        mal_item['synopsis'] =  ' '.join(response.css('p[itemprop=description]::text').getall()[:-2])
        mal_item['link'] = response.css('div.di-ib a::attr(href)').getall()[-2]

        yield mal_item


    def episode_parse(self, response):

        mal1_item = Mal1Item()

        mal1_item['episode'] = response.css('td.episode-number.nowrap::text').getall()

        if mal1_item['episode'] == []:
            main_page_link = response.css('div[id=horiznav_nav] a::attr(href)').get()
            yield response.follow(url = main_page_link, callback = self.lone_episode_parse)
        else:
            mal1_item['episode'] = response.css('td.episode-number.nowrap::text').getall()
            mal1_item['episode_title'] = response.css('td.episode-title.fs12 a[href]::text').getall()
            mal1_item['episode_date_aired'] = response.css('td.episode-aired.nowrap::text').getall()
            mal1_item['episode_score'] = response.css('td.episode-poll.ac.nowrap.scored div.average span.value::text').getall()
            mal1_item['jp_title'] = response.css('h1.title-name::text').get()

            yield mal1_item


    def lone_episode_parse(self, response):

        mal1_item = Mal1Item()

        date = []
        episode_date = response.css('div.spaceit_pad::text').getall()
        for item in episode_date:
            if re.search('^\n..[a-z]+.[0-9]+..[0-9]+', item, flags=re.IGNORECASE) is not None:
                date.append(item.strip())
        mal1_item['episode_date_aired'] = date
        mal1_item['episode'] = '1'
        mal1_item['episode_score'] = 'N/A'
        mal1_item['jp_title'] = response.css('h1.title-name.h1_bold_none strong::text').get()
        mal1_item['episode_title'] = 'N/A'

        yield mal1_item


if __name__ == '__main__':
    pass