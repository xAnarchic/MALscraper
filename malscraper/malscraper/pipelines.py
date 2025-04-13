# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class MalscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # setting 'N/A' to anime with no english title available
        eng_title = adapter.get('eng_title')
        if eng_title[0] == None:
            adapter['eng_title'] = 'N/A'
        else:
            adapter['eng_title'] = eng_title[0]

        jp_title = adapter.get('jp_title')
        adapter['jp_title'] = jp_title[0]

        show_type = adapter.get('show_type')
        adapter['show_type'] = show_type[0]

        return item

class ImportToMySQLPipeline:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'ShadowHunter44!12',
            database = 'malanime'
        )

        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS anime(
                id int NOT NULL auto_increment,
                jp_title VARCHAR(255),
                eng_title VARCHAR(255),
                episode_num VARCHAR(255),
                show_type VARCHAR(255),
                primary key (id)
                )""")

    def process_item(self, item, spider):

        self.cursor.execute("""
            INSERT into anime(
                jp_title,
                eng_title,
                episode_num,
                show_type)
                values(%s, %s, %s, %s)""", (
            item['jp_title'],
            item['eng_title'],
            item['episode_num'],
            item['show_type']
        ))

        self.connection.commit()
        return item

    def close_spider(self,spider):

        self.cursor.close()
        self.connection.close()