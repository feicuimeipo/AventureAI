import json
import uuid
from datetime import datetime

from sqlalchemy import select, func, or_, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import aliased

from database.db_conn import auto_db_session, readonly_db_session
from database.entity.PlatformCofounderNeed import PlatformCofounderNeedModel
from database.entity.PlatformMatchResults import PlatformMatchResultModel
from database.entity.PlatformUser import PlatformUserModel
from database.entity.PlatformUserProfile import PlatformUserProfileModel


def get_es_unsynchronization_user_profile(user_id):
    with readonly_db_session() as session:
        User = aliased(PlatformUserModel, name='u')
        Profile = aliased(PlatformUserProfileModel, name="p")

        query = session.query(User.user_id,
                              Profile.display_name,
                              Profile.city,
                              Profile.title,
                              Profile.skill_tags,
                              Profile.industry_tags,
                              Profile.completeness,
                              Profile.project_name,
                              Profile.project_stage,
                              Profile.funding_stage,
                              Profile.team_size,
                              Profile.need_tags,
                              Profile.investment_tags,
                              Profile.bio,
                              User.token_count,
                              User.phone,
                              User.email,
                              User.role,
                              User.is_verified,
                              User.lang_pref,
                              User.status).join(Profile, Profile.user_id == User.user_id)

        if user_id:
            query = query.filter(func.coalesce(Profile.es_update_at, datetime.min) < Profile.updated_at)
        else:
            query = query.filter(Profile.user_id == user_id)

        results = query.all()
        rows = results
        return rows


def get_user_profile(user_id=None,type="transform_to_milvus"):
    with readonly_db_session() as session:
        User = aliased(PlatformUserModel, name='u')
        Profile = aliased(PlatformUserProfileModel, name="p")

        query = session.query(User.user_id,
                              User.role,
                              User.is_verified,
                              User.lang_pref,
                              User.status,
                              Profile.display_name,
                              Profile.city,
                              Profile.skill_tags,
                              Profile.industry_tags,
                              Profile.project_name,
                              Profile.project_stage,
                              Profile.funding_stage,
                              Profile.team_size,
                              Profile.need_tags,
                              Profile.investment_tags,
                              Profile.bio,
                              Profile.title,
                              Profile.embedding,
                              Profile.profile_data
                              ).join(Profile, Profile.user_id == User.user_id)
        if user_id:
            query = query.filter(Profile.user_id == user_id)
            results = query.first()
            ret = results
            return [ret]
        elif type == "transform_to_milvus":
                query = query.filter(or_(Profile.updated_at > Profile.embedding_update_at,Profile.embedding_update_at == None, Profile.embedding == None))
                results = query.all()
                ret = results
                return ret
        elif type == "partner_match":
            query = query.filter(
                or_(Profile.updated_at > Profile.partner_match_at, Profile.partner_match_at == None))
            results = query.all()
            ret = results
            return ret


# def get_unfilled_embedding_cofounder_needs(need_id: str):
#     with readonly_db_session() as session:
#         Need = aliased(PlatformCofounderNeedsModel, name="n")
#         query = session.query(Need)
#
#         if need_id:
#             query = query.filter(func.coalesce(Need.embedding_update_at, datetime.min) < Need.update_at)
#         else:
#             query = query.filter(Need.id == need_id)
#
#         rows = query.all()
#         ret = rows
#         return ret


def get_cofounder_need(need_id=None):
    with readonly_db_session() as session:
        Need = aliased(PlatformCofounderNeedModel, name="n")
        stmt = select(Need)
        if need_id:
            stmt = stmt.where(Need.id == need_id)
        else:
            stmt = stmt.where(or_(Need.update_at >= Need.match_update_at, Need.match_update_at == None))
        result = session.execute(stmt)

        rows = result.scalars().all()

        return rows


def update_user_profile_embedding(users):
    with auto_db_session() as session:
        updates = []
        for profile in users:
            if profile.embedding and len(profile.embedding)>0:
                embedding_json =profile.embedding
                updates.append(
                    {"user_id": profile.user_id, "embedding": embedding_json, "embedding_update_at": datetime.now()}
                )
        session.bulk_update_mappings(PlatformUserProfileModel, updates)


def update_user_profile_match_datetime(users):
    with auto_db_session() as session:
        updates = []
        for profile in users:
            if len(profile.embedding)>0:
                updates.append(
                    {"user_id": profile.user_id, "partner_match_at": datetime.now()}
                )
        session.bulk_update_mappings(PlatformUserProfileModel, updates)
        #session.query(PlatformUserProfileModel).where(a=1)


def insert_match_results(dataList,source):
    with auto_db_session() as session:
        ids = []
        datas = []
        for row in dataList:
            if source == "cofounder_need":
                ids.append(str(row.need_id))
            elif source == "user_profile":
                ids.append(str(row.seeker_id))
            data = {
                "id": row.id,
                "seeker_id": row.seeker_id,
                "candidate_id": row.candidate_id,
                "need_id": row.need_id,
                "score_total": row.score_total,
                "score_detail": row.score_detail,
                "reasons": row.reasons,
                "computed_at": datetime.now(),
                "is_featured": row.is_featured,
                "match_resource": source,
                "algo_version": row.algo_version,
            }
            datas.append(data)

        ids = set(ids)
        if source == "cofounder_need":
            session.query(PlatformMatchResultModel).filter(PlatformMatchResultModel.need_id in (ids)).delete(synchronize_session=False)
        elif source == "user_profile":
            session.query(PlatformMatchResultModel).filter(PlatformMatchResultModel.seeker_id in (ids)).delete(synchronize_session=False)

        # 转换函数
        # def orm_to_dict(obj):
        #     return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        stmt = insert(PlatformMatchResultModel).values(datas)
        stmt = stmt.on_conflict_do_update(
            index_elements = ['seeker_id','candidate_id','need_id'],
            set_= {
                "id": stmt.excluded.id,
                "seeker_id": stmt.excluded.seeker_id,
                "candidate_id": stmt.excluded.candidate_id,
                "need_id": stmt.excluded.need_id,
                "score_total": stmt.excluded.score_total,
                "score_detail": stmt.excluded.score_detail,
                "reasons": stmt.excluded.reasons,
                "computed_at": datetime.now(),
                "is_featured": stmt.excluded.is_featured,
                "match_resource": source,
                "algo_version": stmt.excluded.algo_version,
        })
        session.execute(stmt)
        # session.bulk_insert_mappings(PlatformMatchResultModel, dict_list)

def update_cofounder_embedding_status(needs):
    with auto_db_session() as session:
        now = datetime.now()
        updates = []
        for need in needs:
            # embedding_json = json.dumps(need.embedding)
            updates.append(
                {"id": need.id, "embedding": need.embedding, "embedding_update_at": now,"partner_match_at": now}
            )
            session.bulk_update_mappings(PlatformCofounderNeedModel, updates)