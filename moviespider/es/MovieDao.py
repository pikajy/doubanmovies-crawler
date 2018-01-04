
import logging
from elasticsearch_dsl import DocType, String, Object, Nested, InnerObjectWrapper
# from elasticsearch_dsl.field import Long
# from elasticsearch.helpers import scan
# from elasticsearch_dsl.connections import connections
# from elasticsearch_dsl.result import Result

logger = logging.getLogger("MovieDao")


class Comment(InnerObjectWrapper):
    author = String()
    # author = String(analyzer='ik_max_word', search_analyzer='search_analyzer')
    author_profile = String()
    rate = String()
    content = String()
    created_at = String()

class MovieDocType(DocType):
    """
    docType
    """
    movie_id = String()
    directors = String()
    origin = String()
    title = String()
    # category = String(index='not_analyzed')
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
    comments = Nested(doc_class=Comment)

    class Meta:
        index = 'doubanfilm_v2'
        #index = 'purchase_policy_pool_parsed'
        doc_type = 'movie'

    def add_comments(self, commentItems):
        for item in commentItems:
          self.comments.append(item)


exclude_keys = ["id", "comments"]


class MovieDao:
    def __init__(self):
        pass

    @staticmethod
    def save(origin_item):
        item = {k: origin_item[k] for k in origin_item if k not in exclude_keys}
        doc = MovieDocType(**item)
        doc.add_comments(origin_item['comments'])
        try:
            doc.meta.id = origin_item["id"]
            doc.save()
            logger.info('save to es success1')
            result = "保存到es成功"
        except Exception as e:
            logger.error(e)
            result = "保存到es失败"
        return result
