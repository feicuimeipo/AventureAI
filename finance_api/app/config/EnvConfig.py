# -*- coding: utf-8 -*-
# python-dotenv
import os
from pathlib import Path

from dotenv import load_dotenv
# 全局通用配置
from app import settings

class Config(object):
    def __init__(self,env_file):
        BASE_DIR = Path(__file__).resolve().parent
        # 1. 加载环境变量
        # override=True 确保 .env 文件中的值优先于系统已有环境变量
        # verbose=True 在调试时可打印加载了哪些变量
        result = load_dotenv(dotenv_path=BASE_DIR / env_file, override=True, verbose=False)


# 测试环境
# 大写变量代表常量
class DevConfig(Config):
    def __init__(self):
        super().__init__(".env.dev")


# 生产环境
class ProdConfig(Config):
    def __init__(self):
        super().__init__(".env.prod")


# settings.py里传入的是test，则config返回test
config = {
    "dev": DevConfig,
    "prod": ProdConfig
}

# 全局缓存，避免重复实例化
_config_instance = None

# 假设这段代码在一个函数内部，例如 def get_config():
def current():
    global _config_instance
    if _config_instance is None:
        env_name = settings.env
        config_class = config[env_name]
        # 3. 实例化并缓存
        _config_instance = config_class()
        # return self._instance

def str_to_bool(v)->bool:
    if v is not None and v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    else:
        return False

current()


ENV = os.getenv("ENV")
APP_NAME = os.getenv("APP_NAME")
LOG_LEVEL = os.getenv("LOG_LEVEL")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH")
app_port = os.getenv("APP_PORT")
cors = os.getenv("CORS")
# 数据库
mysql_db_url = os.getenv('MYSQL_DB_URL')
db_url = os.getenv('DB_URL')
db_conn_if_echo = str_to_bool(os.getenv('DB_CONN_IF_ECNO'))
# redis
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASSWORD')
redis_db = os.getenv('REDIS_DB')
# Email
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')  # 或者使用其他端口，例如465（SSL)
email_sender = os.getenv('EMAIL_SENDER')
email_passwd = os.getenv('EMAIL_PASSWORD')
# 登录JWT用的密钥
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
# elasticsearch
ES_URL = os.getenv("ES_URL")
ES_API_KEY = os.getenv("es_api_key")
CERT_FINGERPRINT = os.getenv("CERT_FINGERPRINT")
# _schedule
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
# openai_api_key
IS_MOCK=os.getenv('IS_MOCK')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE')
MILVUS_URI = os.getenv('MILVUS_URI')
MILVUS_TOKEN = os.getenv('MILVUS_TOKEN')
MILVUS_DB = os.getenv('MILVUS_DB')
MILVUS_PEM_PATH = os.getenv('MILVUS_PEM_PATH')


