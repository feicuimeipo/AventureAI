import numpy as np
from pymilvus import MilvusClient, DataType

from common.Logger import getLogger
from database.common import PlatformUserManager

logger = getLogger("milvus_user_profile_manager.py")

class UserProfileVector():
    collection_name = "user_profile_collection"
    DIMENSION = 1536
    milvusClient:MilvusClient = None

    def __init__(self, milvus_client:MilvusClient):
        self.milvusClient = milvus_client
        self._create_collection_if_not_exist()

    # =======================
    # 2. 创建集合 (Collection)
    # =======================
    def _create_collection_if_not_exist(self,dim=1536):
        """
        创建一个新的集合，如果已存在则先删除
        :param milvusClient:
        :param collection_name: 集合名称
        :param dim: 向量维度
        :return: Collection 对象
        """
        # # 检查集合是否存在，若存在则删除
        collection_name = self.collection_name

        if not self.milvusClient.has_collection(collection_name):
            schema = self.milvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
            schema.add_field(field_name="user_id", datatype=DataType.VARCHAR, is_primary=True, max_length=64, description="业务用户ID，必填，无默认值")
            schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=self.DIMENSION),
            schema.add_field(field_name="role", datatype=DataType.VARCHAR, max_length=64, nullable=True)
            schema.add_field(field_name="city", datatype=DataType.VARCHAR, max_length=64,  nullable=True)

            # 3. Prepare index parameters
            # STL_SORT是Milvus中用于数值和布尔类型标量字段的排序索引‌
            # Trie‌：专为字符串设计，优化精确匹配和前缀查询（如 name LIKE 'abc%'），适合标签、分类等场景。
            # BITMAP‌：仅适合低基数字段（如状态、类别），UUID的高基数会导致内存占用剧增，性能急剧下降
            # INVERTED
            index_params = self.milvusClient.prepare_index_params()
            index_params.add_index(field_name="user_id", index_type="INVERTED")
            index_params.add_index(field_name="embedding",index_type="IVF_FLAT", metric_type="COSINE") # 可选: COSINE, L2, IP
            index_params.add_index(field_name="role", index_type="BITMAP")
            index_params.add_index(field_name="city", index_type="BITMAP")

            # # 5. Create a collection & index & partition
            self.milvusClient.create_collection(collection_name,schema=schema,dimension=self.DIMENSION)
            self.milvusClient.create_index(collection_name,index_params)
            for role in PlatformUserManager.UserRoleEnum:
                self.milvusClient.create_partition(collection_name,f'role_'+role.value)

            logger.info(f"📦 集合 '{collection_name}' 创建成功")
        logger.info(f"{collection_name} 数据集：{self.milvusClient.get_collection_stats(collection_name)}")

    # =======================
    # 5. 加载集合 (Load)
    # =======================
    def load_collection(self):
        """
        将集合加载到内存中以支持搜索
        :param milvusClient:
        :param collection_name: collection_name 表名
        """
        self.milvusClient.load_collection(collection_name=self.collection_name)
        logger.info("💾 集合已加载到内存")


    # 假设 collection 名为 'users'，包含 'user_id' 和 'embedding' 字段
    # user_id, embedding,status
    def insert_or_update(self,userProfiles):
        #self.load_collection() # 查询是否已存在该 user_id
        userIds=[]
        rows = []
        for profile in userProfiles:
            userIds.append(str(profile.user_id))
            rows.append({"user_id": str(profile.user_id),
                         "embedding": np.array(profile.embedding).astype(np.float32).tolist(),
                         "role": str(profile.role),
                         "city": profile.city
                         })

        self.load_collection()  # 查询是否已存在该 user_id
        res = self.milvusClient.upsert(
            collection_name= self.collection_name,
            data = rows,
        )

        # 3. 获取结果
        # upsert 返回 MutationResult，包含 upsert_count (插入+更新的总数)
        if hasattr(res, 'upsert_count'):
            total_count = res.upsert_count
        elif isinstance(res, dict):
            total_count = res.get('upsert_count', 0)
        else:
            total_count = len(rows)  # 兜底

        logger.info(f"Upsert 完成，影响记录数: {total_count}")
        return total_count


    # =======================
    # 6. 向量搜索 (Search)
    # =======================
    def search_vectors(self, query_embedding, top_k=5, filter_expr=None):
        """
        执行向量相似性搜索，‌性能调优‌：对于高并发场景，考虑使用 async_search 或调整 nprobe/ef 参数以平衡召回率和延迟。
        :param query_embedding: 查询向量
        :param top_k: 返回最相似的 K 个结果,
        :param filter_expr: 标量过滤表达式, 例如 "city == 'Beijing' and role in ['admin', 'user']"。确保字段名和类型与 Schema 定义一致。
        :return: 搜索结果
        """
        # 确保 search_params 中的 metric_type 与创建集合/索引时指定的完全一致，否则搜索结果无意义。
        """
        metric_type:  使用余弦相似度
        nprobe: 表示在搜索时，查询向量会访问多少个最近的聚类中心（Voronoi cells） 
            ‌性能与精度的权衡‌： 
            . 值越大‌：搜索精度越高（召回率更高），但延迟增加，搜索速度变慢。
            . ‌值越小‌：搜索速度越快，但可能遗漏部分相似向量，导致精度下降。
            . ‌默认值‌：通常为 1 或 10，具体取决于客户端 SDK 的默认设置。
            . ‌调优建议‌：nprobe 的值不应超过索引构建时的 nlist（聚类中心数量）。一般建议从较小值开始测试，逐步增加直到满足业务的召回率要求。
            . "nprobe": 10 表示探测10个聚类单元
            IVF（Inverted File Index，倒排索引）类索引家族中的关键参数。适用于 IVF_FLAT、IVF_SQ8、IVF_PQ 等基于聚类的索引类型。如果是HNSW或FLAT索引，此参数可能被忽略或替换为其他参数(如 ef)
            IVF: IVF_FLAT / IVF_SQ8 / IVF_PQ - L2, IP, COSINE -> 常用聚类索引，需配合 nprobe 参数
            NSW: HNSW 索引‌，应将 params 改为 {"ef": 64} 或其他适合 HNSW 的参数。  图索引
            FLAT 索引‌，则不需要 nprobe 参数，因为它是暴力搜索，会遍历所有向量。、
            Binary Index (如 BIN_IVF_FLAT) -二进制向量索引
            - radius: 相似度阈值的核心参数，
        """
        search_params = {
            "metric_type": "COSINE",
            "params":  {
                "nprobe": 10,
                # "radius": 0.5, #设定最小相似度为 0.7
                # "range_filter": 0.9  #可选：设定最大相似度为 0.35，即只返回 0.35-0.9 之间的结果
                }
        }

        try:
            # 执行搜索
            results = self.milvusClient.search(
                collection_name=self.collection_name,
                data=[query_embedding], # 传入查询向量，注意必须包裹在列表中，即使只查一个向量
                anns_field="embedding",  # 指定参与向量相似度计算的字段
                params =search_params,  # 搜索参数 - 包含索引类型特定的参数（如 nprobe for IVF, ef for HNSW）和度量类型（metric_type）
                limit=top_k,  ## 返回前 K 个结果
                exprs=filter_expr, ## 标量过滤表达式，如 "city == 'Beijing'"
                output_fields= ["role","city"]  # 返回额外字段
            )

            processed_results = []
            # 打印结果
            for hits in results:
                if not hits:
                    logger.warning("No matches found for the query.")
                    continue
                for hit in hits:
                    # 提取关键信息
                    item = {
                        "user_id": hit.id,
                        "distance": hit.distance, #这里就是相似度得分/距离
                        "city": hit.entity.get("city"),
                        "role": hit.entity.get("role"),
                    }
                    logger.info(f"ID: {item['user_id']}, Distance: {item['distance']:.4f}, City: {item['city']}, Role: {item['role']}")
                    processed_results.append(item)

            return processed_results
        except Exception as e:
            logger.error(f"查询失败: {str(e)}")
            raise e

    # =======================
    # 7. 清理资源 (Drop)
    # =======================
    def cleanup(self):
        self.milvusClient.close()
        logger.info("🔌 已断开连接")


# =======================
# 主程序入口
# =======================
# if __name__ == "__main__":
#     DIM = 128
#     COLLECTION_NAME = "user_profile_connection"
#
#     # 创建实例,并 创建集合 + 字段 + 索引
#     userProfileVector: UserProfileVector = None
#     try:
#         # 1. 连接
#         milvusClient = getMilvusClient()
#
#         # 创建实例,并 创建集合 + 字段 + 索引
#         userProfileVector = UserProfileVector(milvusClient)
#
#            # 3. 插入数据 - 存在则插入
#         # ids = insert_unique_record(milvus_connect,COLLECTION_NAME,[...], dim=DIM)
#
#         # 5. 加载集合
#         userProfileVector.load_collection()
#
#         # 6. 执行搜索
#         print("\n🔍 开始搜索...")
#        #  query_vec = np.random.random((1, DIM)).astype(np.float32)
#         # search_vectors(milvus_connect,COLLECTION_NAME, query_vec, top_k=3)
#
#         # 7. 带过滤条件的搜索
#         # print("\n🔍 带过滤条件的搜索 (label == 'label_1')...")
#         # search_vectors(milvus_connect,COLLECTION_NAME, query_vec, top_k=3, filter_expr="label == 'label_1'")
#
#     except Exception as e:
#         print(f"发生错误: {e}")
#     finally:
#         if userProfileVector is not None:
#             userProfileVector.cleanup()