# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymysql
from pymysql import IntegrityError

logger = logging.getLogger('MoviespiderPipeline')


class MoviespiderPipeline(object):
    conn = pymysql.connect(host='git.weineel.top', user='root', password='102938', port=3306,
                           database='film', charset="utf8")

    def process_item(self, item, spider):
        # logger.info(item)
        try:
            cur = self.conn.cursor()
            cur.execute(r"insert into doubanfilm(movie_id, origin, title, category, link, cover, rate, casts, detail, "
                        r"screenwriter, language, contury, onview_date, duration, alias, imdb_id, imdb_link, directors)"
                        r"values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                            item.get('movie_id', ''),
                            item.get('origin', ''),
                            item.get('title', ''),
                            item.get('category', ''),
                            item.get('link', ''),
                            item.get('cover', ''),
                            item.get('rate', ''),
                            item.get('casts', ''),
                            item.get('detail', ''),
                            item.get('screenwriter', ''),
                            item.get('language', ''),
                            item.get('contury', ''),
                            item.get('onview_date', ''),
                            item.get('duration', ''),
                            item.get('alias', ''),
                            item.get('imdb_id', ''),
                            item.get('imdb_link', ''),
                            item.get('directors', '')
                        ))
            self.conn.commit()
        except IntegrityError as e:
            logger.error(e)
        return item


# 'movie_id': item.get('movie_id', ''),
#             'origin': item.get('origin', ''),
#             'title': item.get('title', ''),
#             'category': item.get('category', ''),
#             'link': item.get('link', ''),
#             'cover': item.get('cover', ''),
#             'rate': item.get('rate', ''),
#             'casts': item.get('casts', ''),
#             'detail': item.get('detail', ''),
#             'screenwriter': item.get('screenwriter', ''),
#             'language': item.get('language', ''),
#             'contury': item.get('contury', ''),
#             'onview_date': item.get('onview_date', ''),
#             'duration': item.get('duration', ''),
#             'alias': item.get('alias', ''),
#             'imdb_id': item.get('imdb_id', ''),
#             'imdb_link': item.get('imdb_link', '')
