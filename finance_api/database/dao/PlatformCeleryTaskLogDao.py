import datetime
import uuid

from database.db_conn import auto_db_session
from database.entity.PlatformCeleryTaskLog import PlatformCeleryTaskLogModel

"""
使用 _schedule inspect active 快速查看当前卡在哪个任务
部署 Celery Flower‌，配合 Nginx 权限控制，提供可视化的全局视图。
结合 Events API 或 Flower 的 webhook 功能，在任务失败时触发即时通知
定期观察 inspect stats 中的 total 计数和 Redis 队列长度，评估系统负载

Flower 是基于 Python 开发的 Celery 实时监控和管理工具，得益于 Python 的跨平台特性，它能够在 Windows、macOS 和 Linux 上无缝部署
# 基础启动
_schedule -A your_project._schedule flower

# 指定端口启动（默认端口为 5555）
_schedule -A your_project._schedule flower --port=5555
"""
def batchInsertCeleryLog(tasklogList):
    with auto_db_session() as session:
        dict_list = []
        for tasklog in tasklogList:
            data = {
                "task_id":tasklog.task_id,
                "task_name":tasklog.task_name,
                "status":tasklog.status,
                "create_at":tasklog.create_at,
                "desc":tasklog.desc,
            }
            dict_list.append(data)
        session.bulk_insert_mappings(PlatformCeleryTaskLogModel,dict_list)

def insertCeleryLog(task_id,task_name,task_status,desc=None):
    with auto_db_session() as session:
        tasklogEntity = PlatformCeleryTaskLogModel()
        tasklogEntity.task_id = task_id
        tasklogEntity.create_at = datetime.datetime.now(datetime.UTC)
        tasklogEntity.task_name = task_name
        tasklogEntity.status = task_status
        if desc:
            tasklogEntity.desc = desc

        with auto_db_session() as session:
            session.add(tasklogEntity)

# tasklogList = []
# p1 = PlatformCeleryTaskLogModel()
# p1.task_id = uuid.uuid4()
# p1.task_name = 'transform_user_profile_into_milvus'
# p1.create_at = datetime.datetime.now(datetime.UTC)
# tasklogList.append(p1)
#
# p2 = PlatformCeleryTaskLogModel()
# p2.task_id = uuid.uuid4()
# p2.task_name = 'transform_user_profile_into_milvus'
# p2.create_at = datetime.datetime.now(datetime.UTC)
# tasklogList.append(p2)
#
# batchInsertCeleryLog(tasklogList)
