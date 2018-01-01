# 导出模块
# from .SpiderWebItemDao import YTDSpiderWebItemDao
import logging
# 配置 es 连接的全局配置
from elasticsearch_dsl.connections import connections
log = logging.getLogger('es')
log.info('es 连接的全局配置')
connections.create_connection(hosts="http://115.28.224.78:9200", timeout=20)

# 可以通过别名配置多个 ES
# connections.configure(
#     default={'hosts': 'localhost'},
#     dev={
#         'hosts': ['esdev1.example.com:9200'],
#         'sniff_on_start': True
#     }
# )
