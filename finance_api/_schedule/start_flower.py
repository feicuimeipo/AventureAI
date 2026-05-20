


import os
import subprocess
import sys
from common.Logger import getLogger

logger = getLogger("flower")

def get_project_root(project_name:str):
    # 逐级向上查找，直到找到包含项目标识的目录（如项目名、__init__.py等）
    project_root = os.path.dirname(os.path.abspath(__file__))
    while os.path.basename(project_root) != project_name:  # 替换为你的项目名称
        project_root = os.path.dirname(project_root)
        if project_root == "/":  # 避免无限递归到根目录
            break
    return project_root


def main():
    """
    @echo off
    cd D:\\er-yan\\finance_api
    rem celery -A _schedule.celery_app:celery_app flower --address=0.0.0.0 --port=5555 --broker=redis://:123654@47.99.219.51:6379/0
    celery -A _schedule.celery_app:celery_app flower --address=127.0.0.1 --port=5555
    rem --broker=redis://:123654@47.99.219.51:6379/0 --result-backend=redis://:123654@47.99.219.51:6379/1 --broker-connect-timeout=600 --broker-publish-timeout=600
    rem --basic-auth=username:password
    rem --broker=redis://:123654@47.99.219.51:6379/0
    rem flower -A your_project_name --broker=redis://:password@47.99.219.51:6379/0
    rem celery -A your_app worker \
    rem --broker=redis://:password@host:port/0 \
    rem --result-backend=redis://:password@host:port/1 \
    rem --broker-transport-options="{'socket_connect_timeout': 10, 'socket_timeout': 20}" \
    rem --result-backend-transport-options="{'socket_connect_timeout': 10, 'socket_timeout': 20}"

    """

    try:
        # 构建命令: 移除 -P gevent，使用默认的多进程模型，稳定性更高，兼容性好
        CELERY_BIN = os.path.join(os.path.dirname(sys.executable), 'celery.exe')
        CMD = [CELERY_BIN, "-A", "_schedule.celery_app:celery_app", "flower", "--address=0.0.0.0", "--port=5555"]
        PROJECT_ROOT = get_project_root('finance_api')
        logger.info(f"正在启动 flower...: {' '.join(CMD)}")
        logger.info(f"工作目录: {PROJECT_ROOT}")

        subprocess.call(CMD)
    except KeyboardInterrupt as e:
        logger.error(f"\n启动失败{str(e)}。")


if __name__ == '__main__':
    main()
