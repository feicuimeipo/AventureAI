from elasticsearch import Elasticsearch

from app.config import EnvConfig
from common import Logger
from common.Exception import ElasticSearchErrorException

logger = Logger.getLogger("es_conn.py")

def getESConfig():
    es_config = {
        "hosts": EnvConfig.ES_URL.split(","),  # ES 地址（集群用列表：["node1:9200", "node2:9200"]）
        "api_key": EnvConfig.ES_API_KEY,
        #"basic_auth": (EnvConfig.ES_USER, EnvConfig.ES_PWD),  # 认证
        "connections_per_node": 10,  # 连接池大小（避免频繁创建连接）
        "request_timeout": 30,  # 超时时间（聚合分析可能耗时较长）
        "max_retries": 10,  # 最大重试次数
        "retry_on_timeout": True,  # 超时自动重试
        "verify_certs": True,
        #"ca_certs": 'http_ca.crt'
        "ssl_assert_fingerprint":EnvConfig.CERT_FINGERPRINT,
    }
    return es_config

def getESClient():
    # 1. 配置连接参数
    es_config = getESConfig()

    # 2. 建立连接
    es = Elasticsearch(**es_config)

    # 3. 验证连接（必做，避免后续操作失败）
    if es.ping():
        info = es.info()
        health = es.health_report()
        logger.info("连接到es:{}. \t 健康状态：{}".format(info,health))
        return es
    else:
        raise ElasticSearchErrorException("Elasticsearch connection failed")

