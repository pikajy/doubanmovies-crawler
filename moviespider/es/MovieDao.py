# -*- coding: utf-8 -*-

import logging
from elasticsearch_dsl import DocType, String, Object, InnerObjectWrapper
# from elasticsearch_dsl.field import Long
# from elasticsearch.helpers import scan
# from elasticsearch_dsl.connections import connections
# from elasticsearch_dsl.result import Result

logger = logging.getLogger("MovieDao")


class MovieDocType(DocType):
    """
    docType
    """
    movie_id = String()
    directors = String()
    origin = String()
    title = String()
    category = String()
    link = String()
    cover = String()
    rate = String()
    casts = String()
    status = String()
    detail = String()
    screenwriter = String()
    language = String()
    contury = String()
    onview_date = String()
    duration = String()
    alias = String()
    imdb_id = String()
    imdb_link = String()

    # region = Object(doc_class=Region)  # 区域

    class Meta:
        index = 'doubanfilm'
        #index = 'purchase_policy_pool_parsed'
        doc_type = 'movie1'

    # def set_region(self, **region):
    #     """
    #     设置所在位置
    #     :param region:
    #     """
    #     self.region["district"] = region["district"]
    #     self.region["province"] = region["province"]
    #     self.region["city"] = region["city"]


exclude_keys = ["id"]


class MovieDao:
    def __init__(self):
        pass

    @staticmethod
    def save(origin_item):
        item = {k: origin_item[k] for k in origin_item if k not in exclude_keys}
        doc = MovieDocType(**item)
        try:
            doc.meta.id = origin_item["id"]
            doc.save()
            logger.info('save to es success1')
            result = "保存到es成功"
        except Exception as e:
            logger.error(e)
            result = "保存到es失败"
        return result
