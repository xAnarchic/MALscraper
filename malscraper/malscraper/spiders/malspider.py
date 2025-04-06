# Spider

import scrapy
import sys
import re

class MALSpider(scrapy.Spider):
    name = 'malspider'
    allowed_domains = ['myanimelist.net']
    start_urls = ['https://myanimelist.net/topanime.php']   # orders all anime on the website by score

    def parse(self, response):
        animes = response.css('tr.ranking-list')    # returns a list of the 50 anime found on each page

        for anime in animes:    # iterating through each anime to get information

            relative_url = anime.css('h3.fl-l.fs14.fw-b.anime_ranking_h3 a::attr(href)').get()
            yield response.follow(relative_url, callback=self.parse_anime)

        next_page = response.css('div.di-b.ac.pt16.pb16.pagination.icon-top-ranking-page-bottom a::attr(href)').getall()[-1]  # specifically gets the link to the next page of anime, avoids the "prev page" link
        next_page_url = 'https://myanimelist.net/topanime.php' + next_page

        if next_page_url != None:
            yield response.follow(next_page_url, callback = self.parse)
        else:
            print('All pages scraped. Script will now be terminated')
            sys.exit




    def parse_anime(self, response):

        info = response.css('div.spaceit_pad::text').getall()   # list of info about anime
        for item in info:   # iterating over items in the list
            if re.search('[0-9]+', item) != None:   # looking for an item with numbers inside ------- try to find a pattern specific to the episode info, like spaces, starting characters, ending characters, etc
                episode = item  # assigns item with the 'episode' variable
                break   # as soon as an item is found, the loop ends


        yield {
            'jp title' : response.css('h1.title-name.h1_bold_none strong::text').get(),
            'eng title' : response.css('p.title-english.title-inherit::text').get(),
            'show type' : response.css('div.spaceit_pad a::text').getall()[0],
            'episodes' :  episode    # needs regex to only return numbers
        }


# if __name__ == '__main__':
#     pass


