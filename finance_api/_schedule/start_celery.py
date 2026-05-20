import os
import subprocess
import sys

from _schedule import init_task
from common.Logger import getLogger

logger = getLogger("_schedule")

def get_project_root(project_name):
    # 逐级向上查找，直到找到包含项目标识的目录（如项目名、__init__.py等）
    project_root = os.path.dirname(os.path.abspath(__file__))
    while os.path.basename(project_root) != project_name:  # 替换为你的项目名称
        project_root = os.path.dirname(project_root)
        if project_root == "/":  # 避免无限递归到根目录
            break
    return project_root


def main():
    """
    在Windows环境下启动Celery Worker。
    注意：必须使用 -P eventlet 或 -P gevent 池，因为默认的 prefork 池在Windows上不支持。d


# 先获取当前机器IP（Windows可在cmd中执行ipconfig，Linux/macOS执行ifconfig）
python -m celery -A MyApp worker \
    --loglevel=info \
    --broker=redis://:your_password@47.99.219.51:6379/0 \
    --result-backend=redis://:your_password@47.99.219.51:6379/1 \
    --concurrency=4 \
    --pool=gevent \
    --worker-name=你的IP地址  # 替换为实际IP，如192.168.1.100

    """
    logger.info("正在检查 gevent 是否安装...")
    try:
        import gevent
    except ImportError:
        logger.error("错误: 未找到 eventlet。请先运行 'pip install gevent'")
        sys.exit(1)

    try:
        # 构建命令: 移除 -P gevent，使用默认的多进程模型，稳定性更高，兼容性好
        CELERY_BIN = os.path.join(os.path.dirname(sys.executable), 'celery.exe')
        CMD = [CELERY_BIN, "-A", "_schedule.celery_app:celery_app", "worker", "-l", "info", "-P", "gevent","--concurrency=4","--hostname=192.168.1.6"]
        # CMD = [CELERY_BIN, "-A", "_schedule.celery_app:celery_app", "worker", "-l", "info", "-P", "prefork", "--concurrency=4", "--hostname=192.168.1.6"]
        PROJECT_ROOT = get_project_root('finance_api')
        logger.info(f"正在启动 Celery Worker...: {' '.join(CMD)}")
        logger.info(f"工作目录: {PROJECT_ROOT}")

        subprocess.call(CMD)
    except KeyboardInterrupt as e:
        logger.error(f"\n启动失败{str(e)}。")


if __name__ == '__main__':
    main()
