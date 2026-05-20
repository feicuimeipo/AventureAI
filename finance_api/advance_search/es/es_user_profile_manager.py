from elasticsearch import helpers

from advance_search.es import es_conn
from common import Logger

logger = Logger.getLogger("my_elasticsearch_client")
class UserProfileES(object):
    index_name = 'venturo_ai_user_profiles'
    index_mapping = {
        "mappings": {
            "properties": {
                "user_id": {"type": "keyword"},  # 维度：用户ID（去重统计）
                "city": {"type": "keyword"},  # 维度：城市（分组）
                "skill_tags": {"type": "keyword"},  # 维度：城市（分组）
                "industry_tags": {"type": "keyword"},  # 维度：城市（分组）
                "project_name": {"type": "text"},  # 维度：项目名
                "project_stage": {"type": "keyword"},  # 维度：项目名
                "funding_stage": {"type": "keyword"},  # 维度：项目名
                "team_size": {"type": "integer"},  # 维度：项目名
                "need_tags": {"type": "keyword"},  # 维度：项目名
                "investment_tags": {"type": "keyword"},  # 维度：项目名
                "role": {"type": "keyword"},  # 维度
                "title": {"type": "keyword"}, # 岗位
                "activity_coefficient": {"type": "keyword"}  #活跃度系数(
            }
        }
    }
    def __init__(self,es_client=None):
        if es_client:
            self.es_client = es_client
        else:
            self.es_client = es_conn.getESClient()
        if not self.es_client.indices.exists(index=self.index_name):
            logger.info("{}索引不存在，在线创建索引".format(self.index_name))
            #ResourceAlreadyExistsException
            self.es_client.indices.create(index=self.index_name, body=self.index_mapping)

    def _prepare_bulk_actions(self,data_list):
        """
        生成用于 bulk API 的动作列表，将业务字段 'biz_id' 设为文档 _id
        :param data_list: 包含字典的列表，每个字典必须包含 'biz_id'
        :param index_name: 目标索引名称
        :return: 动作生成器
        """
        for item in data_list:
            # 提取业务唯一ID，确保转换为字符串，因为 _id 必须是字符串
            doc_id = str(item.get('user_id'))
            if not doc_id:
                continue  # 跳过没有业务ID的数据
            # 构造动作元数据
            action = {
                "_index": self.index_name,
                "_id": doc_id,  # 关键：将业务ID赋值给 _id
                "_source": item  # 文档主体
            }
            yield action


    def bulkDocument(self,data_list):
        es_datas = []
        for row in data_list:
            # 定义索引映射
            dict = {}
            dict['user_id'] = row.user_id
            dict['city'] = row.city
            dict['title'] = row.title
            dict['skill_tags'] = row.skill_tags
            dict['industry_tags'] = row.industry_tags
            dict['project_name'] = row.project_name
            dict['project_stage'] = row.project_stage
            dict['funding_stage'] = row.funding_stage
            dict['team_size'] = row.team_size
            dict['need_tags'] = row.need_tags
            dict['investment_tags'] = row.investment_tags
            dict['role'] = row.role

            es_datas.append(dict)

        action = self._prepare_bulk_actions(es_datas)
        try:
            success, failed = helpers.bulk(
                client=self.es_client,
                actions=action,
                chunk_size=500,
                request_timeout=30
            )
            self.es_client.indices.refresh(index=self.index_name)
            logger.error(f"成功写入: {success}, 失败: {failed}")
        except Exception as e:
            logger.error(f"批量写入错误{str(e)}")

    def bulkActivityCoefficient(self,data_list):
        es_datas = []
        for row in data_list:
            # 定义索引映射
            dict = {}
            dict['user_id'] = row.user_id
            dict['activity_coefficient'] = row.activity_coefficient
            es_datas.append(dict)

        action = self._prepare_bulk_actions(es_datas)
        try:
            success, failed = helpers.bulk(
                client=self.es_client,
                actions=action,
                chunk_size=500,
                request_timeout=30
            )
            self.es_client.indices.refresh(index=self.index_name)
            logger.error(f"成功写入: {success}, 失败: {failed}")
        except Exception as e:
            logger.error(f"批量写入错误{str(e)}")

    def insertOrUpdateDocument(self, doc_id, document):
        self.es_client.indices.insert(index=self.index_name, id=doc_id, body=document)


    def deleteDocument(self,doc_id=None):
        self.es_client.indices.delete(index=self, id=doc_id)

    def search(self, query):
        response = self.es_client.indices.search(index=self.index_name, body=query)
        hits = response["hits"]["hits"]
        for hit in hits:
            source = hit["_source"]
            return source
        return None

    """
    ‌小数据量/精确排序‌：使用Painless 脚本‌ (script_score)。
    ‌中等数据量/快速过滤‌：使用 terms_set 查询。
    ‌海量数据/去重推荐‌：使用 MinHash 近似算法 + 脚本重排序。
    方案：根据你的业务场景（如技能匹配、商品推荐），通常推荐组合使用：先用 terms_set 或 terms 快速召回候选集，再用 Painless 脚本计算精确 Jaccard 系数进行最终排序。
    """
    def searchSkill(self, skillReqs:list):
        query = {
            "query": {
                "terms_set": {
                    "skill_tags": {
                        "term": {
                            "skill_tags": {
                                "terms": skillReqs,
                                "boost": 4.0 #25%权重
                            }
                        }
                    }
                }
            }
        }
        response = self.es_client.indices.search(index=self.index_name, body=query)
        hits = response["hits"]["hits"]
        for hit in hits:
            source = hit["_source"]
            return source
        return None