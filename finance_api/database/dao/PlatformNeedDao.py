from datetime import datetime,timedelta

from sqlalchemy import update, and_, desc
from sqlalchemy.orm import aliased

from database.db_conn import auto_db_session, readonly_db_session
from database.entity.PlatformCofounderNeed import PlatformCofounderNeedModel


def insertNeed(entity):
    with auto_db_session() as session:
        entity.status = 'active'
        now = datetime.now()
        entity.created_at = now
        entity.update_at = now
        entity.expired_at = now + timedelta(days=90)

        session.add(entity)


def updateNeed(entity):
    with auto_db_session() as session:
        stmt = (
            update(PlatformCofounderNeedModel)
            .where(PlatformCofounderNeedModel.id == entity.id)
            .values(**entity.to_dict())  # 假设 entity 有 to_dict 方法，或者手动构建字典
        )
        session.execute(stmt)

def getDataLists(user_id):
    NeedModel = aliased(PlatformCofounderNeedModel)
    with readonly_db_session() as session:
        rows = session.query(NeedModel).filter(NeedModel.user_id == user_id).filter(NeedModel.status == 'active')\
                                            .filter(NeedModel.status == 'active')\
                                            .filter(NeedModel.expired_at >= datetime.now())\
                                            .order_by(desc(NeedModel.created_at)).limit(5).all()
        rets = rows
        return rets

def getById(need_id):
    with readonly_db_session() as session:
        row = session.query(PlatformCofounderNeedModel).filter(PlatformCofounderNeedModel.id == need_id).first()
        ret = row
        return ret