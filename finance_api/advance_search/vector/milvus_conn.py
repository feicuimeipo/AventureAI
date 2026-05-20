from pymilvus import MilvusClient

from app.config import EnvConfig
from common.Logger import getLogger

logger = getLogger("milvus_conn.py")

def getMilvusClient() -> MilvusClient:
    """
       连接到 Milvus 服务器
    """
    try:
        MILVUS_URI = EnvConfig.MILVUS_URI
        MILVUS_TOKEN = EnvConfig.MILVUS_TOKEN
        MILVUS_PEM_PATH = EnvConfig.MILVUS_PEM_PATH
        db_name = EnvConfig.MILVUS_DB

        if MILVUS_URI.lower().startswith("https://"):

            username = MILVUS_TOKEN.split(":")[0]
            pwd = MILVUS_TOKEN.split(":")[1]
            client = MilvusClient(
                uri=MILVUS_URI,
                user=username,
                password=pwd,
                server_pem_path = MILVUS_PEM_PATH  # 服务器证书文件路径
            )
            version = client.get_server_version()
            logger.info(f'成功连接到Milvus: {MILVUS_URI}-version:{version}')
        else:
            client = MilvusClient(
                uri=MILVUS_URI,  # 实例公网地址
                token=MILVUS_TOKEN  # 格式：用户名:密码
            )
            version = client.get_server_version()
            logger.info(f'成功连接到 milvus: {MILVUS_URI}-version:{version}')

        if db_name not in client.list_databases():
            logger.info(f"数据库 {db_name}不存在，正在创建...")
            client.create_database(db_name=db_name)
            logger.info(f"数据库 {db_name}，创建成功!")

        client.use_database(db_name=db_name)
        return client
    except Exception as e:
        logger.error(f'连接失败入:{e}')
        raise



