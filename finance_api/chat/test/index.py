import logging
import os
from langchain_openai import OpenAIEmbeddings

from common.Logger import getLogger

# 设置 OpenAI API Key
# 建议通过环境变量设置，例如: export OPENAI_API_KEY="your-api-key"
# documents = [
#         f"角色: {profile.user.role}",
#         f"介绍: {profile.bio}",
#         f"技能: {', '.join(profile.skill_tags)}",
#         f"行业: {', '.join(profile.industry_tags)}",
#         f"城市: {profile.city}"
#     ]
logger = getLogger()
def generate_document_embeddings(documents):
    """
    使用 LangChain 和 OpenAI 生成文档的嵌入向量
    """
    # 1. 初始化 Embeddings 模型
    # 默认使用 text-embedding-3-small 模型，性价比高
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # 2. 准备文档文本列表
    # documents = [
    #     "LangChain 是一个用于开发由语言模型驱动的应用程序的框架。",
    #     "OpenAI 提供了强大的 GPT 系列模型和 Embedding 模型。",
    #     "向量数据库用于存储和检索高维向量数据，支持语义搜索。"
    # ]

    try:
        # 3. 生成嵌入向量
        # embed_documents 方法用于处理多个文本，返回一个二维列表
        vector_list = embeddings.embed_documents(documents)

        # 4. 输出结果示例
        logger.info(f"成功生成 {len(vector_list)} 个文档的嵌入向量。")
        logger.info(f"第一个文档的向量维度: {len(vector_list)}")
        logger.info(f"第一个文档向量的前5个值: {vector_list[:5]}")

        return vector_list

    except Exception as e:
        logger.info(f"生成嵌入向量时出错: {e}")
        return []

if __name__ == "__main__":
    generate_document_embeddings()



