from datetime import datetime

from sqlalchemy import func, select, Date, cast
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import aliased

from common.Logger import getLogger
from database.db_conn import auto_db_session, readonly_db_session
from database.entity import PlatformUserStat
from database.entity.PlatformUserStat import PlatformUserStatModel

logger =getLogger()



def bulkInsertActivity(data_list):
    with auto_db_session() as session:
        if len(data_list)>0:
            stmt = insert(PlatformUserStatModel).values(data_list)
            stmt = stmt.on_conflict_do_update(
                index_elements=['user_id','create_at'],  # 指定触发冲突的唯一列
                set_={
                    'login_count_7days': func.coalesce(stmt.excluded.login_count_7days,PlatformUserStatModel.login_count_7days),
                    'browse_count': func.coalesce(stmt.excluded.browse_count, PlatformUserStatModel.browse_count),
                    'message_count': func.coalesce(stmt.excluded.message_count, PlatformUserStatModel.message_count),
                    'last_active_time': func.coalesce(stmt.excluded.last_active_time, PlatformUserStatModel.last_active_time),
                    'daily_duration': func.least(func.coalesce(stmt.excluded.daily_duration, PlatformUserStatModel.daily_duration), 3600*8),
                    'update_at': func.now()
                }
            )
            user_data = session.execute(stmt) # 或 stmt_do_nothing
            logger.info(f"Successfully upserted {user_data} records.")

def getUserStats(userIds)->list:
    with readonly_db_session() as session:
        stmt = select(PlatformUserStatModel).where(PlatformUserStatModel.user_id.in_(userIds))
        results = session.execute(stmt)
        rows = results.scalars().all()
        return rows