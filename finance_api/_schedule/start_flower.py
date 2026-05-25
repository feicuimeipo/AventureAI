import os
import subprocess
import sys
from common.Logger import getLogger

logger = getLogger()

def get_project_root(project_name:str):
    project_root = os.path.dirname(os.path.abspath(__file__))
    while os.path.basename(project_root) != project_name:  # 替换为你的项目名称
        project_root = os.path.dirname(project_root)
        if project_root == "/":  # 避免无限递归到根目录
            break
    return project_root


def main():
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
