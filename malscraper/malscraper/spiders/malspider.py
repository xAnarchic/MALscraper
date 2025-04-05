# Spider

import scrapy

class MALSpider(scrapy.Spider):
    name = 'malspider'
    allowed_domains = ['myanimelist.net']
    start_urls = ['https://myanimelist.net/topanime.php']   # orders all anime on the website by score

    def parse(self, response):
        animes = response.css('tr.ranking-list')    # returns a list of the 50 anime found on each page

        for anime in animes:    # iterating through each anime to get information
            yield {
                'title' : anime.css('a::text').getall()[-2],
                'rating' : anime.css('span::text').getall()[1],
                'airing time' : anime.css('div.information.di-ib.mt4::text').getall()[1]
            }

        next_page = anime.css('div.di-b.ac.pt16.pb16.pagination.icon-top-ranking-page-bottom')[-1]  # specifically gets the link to the next page of anime, avoids the "prev page" link
        next_page_url = 'https://myanimelist.net/topanime.php' + next_page

        if next_page != None:
            yield response.follow(next_page_url, callback = self.parse)



# if __name__ == '__main__':
#     pass


