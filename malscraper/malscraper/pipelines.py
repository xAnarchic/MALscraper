# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import json
from .items import MalItem, Mal1Item
import re


class MalscraperPipeline:
    def process_item(self, item, spider):
        if isinstance(item, MalItem):
            return self.handle_mal(item, spider)
        if isinstance(item, Mal1Item):
            return self.handle_Mal1Item(item, spider)


    def handle_mal(self, item, spider):

        adapter = ItemAdapter(item)

        # setting 'N/A' to anime with no english title available
        eng_title = adapter.get('eng_title')
        if eng_title[0] is None:
            adapter['eng_title'] = 'N/A'
        else:
            adapter['eng_title'] = eng_title[0]


        genres_themes = adapter.get('genres_themes')

        genres = []
        themes = []
        demographics = []

        all_genres = ['Action', 'Adventure', 'Avant Garde', 'Award Winning', 'Boys Love', 'Comedy', 'Drama', 'Fantasy', 'Girls Love', 'Gourmet', ' Horror', 'Mystery', 'Romance',
                  'Sci-Fi', 'Slice of Life', 'Sports', 'Supernatural', 'Suspense']

        all_demographics = ['Josei', 'Kids', 'Seinen', 'Shoujo', 'Shounen']

        if genres_themes is not None:
            for element in genres_themes:
                if element in all_genres:
                    genres.append(element)
                elif element in all_demographics:
                    demographics.append(element)
                else:
                    themes.append(element)

        if genres == []:
            genres = 'N/A'
        else:
            genres = json.dumps(genres)
            genres = genres.translate(genres.maketrans('', '', '[]"'))

        if themes == []:
            themes = 'N/A'
        else:
            themes = json.dumps(themes)
            themes = themes.translate(themes.maketrans('', '', '[]"'))

        if demographics == []:
            demographics = 'N/A'
        else:
            demographics = json.dumps(demographics)
            demographics = demographics.translate(demographics.maketrans('', '', '[]"'))

        adapter['genres'] = genres
        adapter['themes'] = themes
        adapter['demographics'] = demographics

        jp_title = adapter.get('jp_title')

        adapter['jp_title'] = jp_title[0]

        show_type = adapter.get('show_type')
        adapter['show_type'] = show_type[0]

        synopsis = adapter.get('synopsis')
        if synopsis == '':
            adapter['synopsis'] = 'N/A'
        else:
            adapter['synopsis'] = re.sub('\r\n', '', synopsis)

        studio = adapter.get('studio')
        if studio == '':
            adapter['studio'] = 'N/A'

        return item


    def handle_Mal1Item(self, item, spider):

        adapter = ItemAdapter(item)
        episode = adapter.get('episode')
        adapter['episode_date_aired'] = '-'.join(adapter.get('episode_date_aired'))

        if episode == '1':
            adapter['episode_score'] = 'N/A'
            adapter['episode_title'] = 'N/A'

        elif episode == '' or episode == []:
            adapter['episode'] = 'N/A'
            adapter['episode_score'] = 'N/A'
            adapter['episode_title'] = 'N/A'

        else:
            adapter['episode'] = '-'.join(adapter.get('episode'))
            adapter['episode_score'] = '-'.join(adapter.get('episode_score'))
            adapter['episode_title'] = '---'.join(adapter.get('episode_title'))

        return item


class ImportToMySQLPipeline:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',      # enter account password
            database = ''   # enter name of database
        )

        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS general_anime_info(
                id int NOT NULL auto_increment,
                jp_title VARCHAR(255),
                eng_title VARCHAR(255),
                episode_num VARCHAR(255),
                show_type VARCHAR(255),
                score TEXT,
                ranking INT,
                popularity INT,
                studio VARCHAR(255),
                genres VARCHAR(255),
                themes VARCHAR(255),
                demographics VARCHAR(255),
                synopsis TEXT,
                link TEXT,
                primary key (id)
                )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS episode_anime_info(
                jp_title VARCHAR(255),
                episode TEXT,
                episode_title TEXT,
                episode_score TEXT,
                episode_date_aired TEXT
                )""")

    def process_item(self, item, spider):

        if isinstance(item, MalItem):
            return self.sql_mal(item, spider)
        if isinstance(item, Mal1Item):
            return self.sql_mal1(item, spider)


    def sql_mal(self, item, spider):

        self.cursor.execute("""
                        INSERT into general_anime_info(
                            jp_title,
                            eng_title,
                            episode_num,
                            show_type,
                            score,
                            ranking,
                            popularity,
                            studio,
                            genres,
                            themes,
                            demographics,
                            synopsis,
                            link
                            )
                            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            item['jp_title'],
            item['eng_title'],
            item['episode_num'],
            item['show_type'],
            item['score'],
            item['ranking'],
            item['popularity'],
            item['studio'],
            item['genres'],
            item['themes'],
            item['demographics'],
            item['synopsis'],
            item['link']
        ))

        self.connection.commit()
        return item


    def sql_mal1(self, item, spider):

        self.cursor.execute("""
                         INSERT into episode_anime_info(
                             jp_title,
                             episode,
                             episode_title,
                             episode_score,
                             episode_date_aired
                             )
                             values(%s, %s, %s, %s, %s)""", (
            item['jp_title'],
            item['episode'],
            item['episode_title'],
            item['episode_score'],
            item['episode_date_aired']
        ))

        self.connection.commit()
        return item


    def close_spider(self,spider):

        self.cursor.close()
        self.connection.close()