import socket
from celery import Celery
from celery.schedules import crontab
from flask import Flask
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from app.config import EnvConfig
from common.Logger import getLogger

logger = getLogger()
# 获取当前机器的IP地址
def get_local_ip():
    try:
        # 优先获取局域网IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # 失败则返回127.0.0.1
        return "127.0.0.1"


"""
aiohttp用于异步抓取任务
"""
def make_celery(flask_app:Flask=None):
    # 创建自定义Redis连接池

    """
    创建并配置 Celery 实例，使其支持 Flask 应用上下文
    """
    # 1. 创建 Celery 实例
    celery = Celery(
        EnvConfig.APP_NAME,  # 推荐使用 app.import_name，便于定位任务
        broker= EnvConfig.CELERY_BROKER_URL,
        backend = EnvConfig.CELERY_RESULT_BACKEND,
    )

    # 2. 更新配置
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='Asia/Shanghai',
        enable_utc=False,
        concurrency=4,
        worker_concurrency=4,
        task_default_pool="gevent",
        task_time_limit=30 * 60,  # 30分钟
        task_soft_time_limit=25 * 60,  # 25分钟
        task_routes={
            'tasks.heavy_task': {'queue': 'heavy'},
            'tasks.light_task': {'queue': 'light'},
        },
        result_expires=3600,  # 结果过期时间，单位秒
    )

    celery.broker_pool_limit = 10
    # celery.conf.worker_pool = asyncio  # 关键配置：启用 asyncio 池
    celery.conf.broker_transport_options = {
        'max_connections': 20,
        'socket_connect_timeout': 36,
        'socket_timeout': 60,
        'socket_keepalive': True,  # socket_keepalive 通常是一个布尔值，具体行为取决于驱动
        'retry_policy': {
            'max_retries': 3,
            'interval_start': 0,
            'interval_step': 0.2,
            'interval_max': 0.5,
        }
    }

    celery.conf.backend_transport_options = {
        'max_connections': 10,
        'socket_connect_timeout': 36,
        'socket_timeout': 60,
        'socket_keepalive': True,
    }


    # # 定义定时任务调度表
    celery.conf.beat_schedule = {
        # # 每 60 秒执行一次
        'record_user_stat': {
            'task': 'partner_match_based_on_need',
            #'schedule': 3600.0,
            'schedule': crontab(hour=1),
             #'schedule': crontab(hour=2),
            'args': ()
        }
    }

    # # 定义定时任务调度表
    celery.conf.beat_schedule = {
        # # 每 60 秒执行一次
        'record_user_stat': {
            'task': 'transform_user_profile_into_milvus',
            #'schedule': 3600.0,
            'schedule': crontab(hour=2),
             #'schedule': crontab(hour=2),
            'args': ()
        }
    }

    if flask_app is not None:
        # 3. 【关键】自定义 Task 基类，自动处理应用上下文
        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                # 每次执行任务时，推入 Flask 应用上下文
                # 这样任务内部就可以使用 current_app, db.session 等
                with flask_app.app_context():
                    return self.run(*args, **kwargs)

        # 4. 将自定义的 Task 类设置为 Celery 的默认 Task
        celery.Task = ContextTask

    return celery


# 创建一个默认的celery实例，用于在worker启动时导入任务
celery_app = make_celery() # 全局变量，用于其他地方导入
celery_app.autodiscover_tasks(['_schedule.task_user_profile','_schedule.task_partner_match'])

