"""
text-embedding-3-small: 性价比高，速度快，适合大多数场景。
text-embedding-3-large: 性能最强，适合对精度要求极高的场景。
text-embedding-ada-002: 旧版模型，仍广泛使用，但新版模型在性能
---
OpenAIEmbeddings 提供了两个主要方法：
embed_query: 用于生成单个查询文本的向量（通常用于搜索时的查询端）。
embed_documents: 用于批量生成多个文档文本的向量（通常用于构建知识库时的文档端）。
"""

from langchain_openai import OpenAIEmbeddings

from app.config import EnvConfig
from common.Logger import getLogger

logger = getLogger("embedding_generator.py")

# 余弦相似度
def calculate_semantic_similarity(desc1: str, desc2: str) -> float:
    """
    用向量相似度衡量两段文本的语义接近程度
    """
    api_key = EnvConfig.OPENAI_API_KEY
    openai_api_base = EnvConfig.OPENAI_API_BASE
    if not api_key or not openai_api_base:
        logger.error("未找到 OPENAI_API_KEY 环境变量。")
        return 0

    # 1. 向量化文本（用 OpenAI 的 embedding model）
    embedding1 = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_base = openai_api_base,
        input = desc1
    )['data'][0]['embedding']

    embedding2 = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_base = openai_api_base,
        input = desc2
    )['data'][0]['embedding']

    # 2. 计算余弦相似度
    import numpy as np
    cos_similarity = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
    )

    # 3. 转换成 0-100 的评分
    score = cos_similarity * 100

    return score
