import datetime
import uuid

from sqlalchemy import and_, desc

from database.db_conn import auto_db_session, readonly_db_session
from database.entity.PlatformMatchInteractions import PlatformMatchInteractionModel


def addMatchInteraction(entity: PlatformMatchInteractionModel):
    with auto_db_session() as session:
        session.insert(PlatformMatchInteractionModel).values(entity)
        session.on_conflict_do_nothing(
            index_elements=['from_user_id', 'to_user_id','result_id', 'action' ],
        )
        session.add(entity)

def setMutual(from_user_id,to_user_id,result_id):
    with auto_db_session() as session:
        query = session.query(PlatformMatchInteractionModel).filter(PlatformMatchInteractionModel.from_user_id == from_user_id) \
            .filter(PlatformMatchInteractionModel.to_user_id == to_user_id) \
            .filter(PlatformMatchInteractionModel.result_id == result_id) \
            .order_by(desc(PlatformMatchInteractionModel.created_at)).first()
        if query:
            query.is_mutual = True
            session.execute(query)
        else:
            matchInteraction = PlatformMatchInteractionModel()
            matchInteraction.id = uuid.uuid4()
            matchInteraction.from_user_id = from_user_id
            matchInteraction.to_user_id = to_user_id
            matchInteraction.action = "mutual"
            matchInteraction.is_mutual = False
            matchInteraction.created_at = datetime.datetime.now()
            matchInteraction.result_id = result_id
            session.add(matchInteraction)


def deleteMatchInteraction(from_user_id,to_user_id,result_id,action):
    with auto_db_session() as session:
        stmt = session.delete(PlatformMatchInteractionModel).where(
            and_( PlatformMatchInteractionModel.from_user_id == from_user_id
                 ,PlatformMatchInteractionModel.to_user_id == to_user_id
                  ,PlatformMatchInteractionModel.result_id == result_id
                  ,PlatformMatchInteractionModel.action == action
                )
        )
        session.execute(stmt)


def listInteractionAll(from_user_id,to_user_id,result_id):
    with readonly_db_session() as session:
        rows = session.query(PlatformMatchInteractionModel) \
                .filter(PlatformMatchInteractionModel.from_user_id == from_user_id) \
                .filter(PlatformMatchInteractionModel.to_user_id == to_user_id) \
                .filter(PlatformMatchInteractionModel.result_id == result_id) \
                .all()
        results = rows
        return results

def listInteractionAction(from_user_id,to_user_id,result_id):
    with readonly_db_session() as session:
        rows = session.query(PlatformMatchInteractionModel.action) \
                .filter(PlatformMatchInteractionModel.from_user_id == from_user_id) \
                .filter(PlatformMatchInteractionModel.to_user_id == to_user_id) \
                .filter(PlatformMatchInteractionModel.result_id == result_id) \
                .all()
        results = rows
        return results


