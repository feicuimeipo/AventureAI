# -*- coding: utf-8 -*-
import os
from datetime import datetime

from sqlalchemy import update, or_
from sqlalchemy.orm import aliased

from common.Logger import getLogger
from database.db_conn import auto_db_session, readonly_db_session
from database.entity.PlatformTokenLog import PlatformTokenLogModel
from database.entity.PlatformUser import PlatformUserModel
from database.entity.PlatformUserProfile import PlatformUserProfileModel

logger = getLogger(os.path.basename(__file__))

def findByEmail(account) -> PlatformUserModel:
    with readonly_db_session() as session:
        row = (session.query(PlatformUserModel)
                .filter(PlatformUserModel.email == account).first())
        ret = row
        return ret

def findByPhone(phone):
    with readonly_db_session() as session:
        row = session.query(PlatformUserModel).filter(PlatformUserModel.phone == phone).first()
        ret = row
        return ret

def findByEmailOrPhone(account:str) -> PlatformUserModel:
    with readonly_db_session() as session:
        row = session.query(PlatformUserModel).filter(or_(PlatformUserModel.email == account,PlatformUserModel.phone == account)).first()
        ret = row
        return ret


def findById(userId) -> PlatformUserModel:
    with readonly_db_session() as session:
        row = session.query(PlatformUserModel).filter(PlatformUserModel.user_id == userId).first()
        ret = row
        return ret


def findAllActiveUsers(uid = None):
    User = aliased(PlatformUserModel, name='u')
    Profile = aliased(PlatformUserProfileModel, name="p")
    with readonly_db_session() as session:
        query = session.query(User, Profile) \
                 .join(Profile, User.user_id == Profile.user_id) \
                 .filter(User.status == 'active')
        if uid:
            query.filter(User.user_id == uid)
        rows = query.all()
        results = rows
        return results


def getDetailById(userId):
    with readonly_db_session() as session:
        User = aliased(PlatformUserModel, name='u')
        Profile = aliased(PlatformUserProfileModel, name="p")

        query = (session.query(User,Profile)
                 .join(Profile,User.user_id == Profile.user_id).filter(User.user_id == userId)
                 )
        rows = query.first()
        ret = rows
        return ret


def getProfileById(useId) -> PlatformUserProfileModel:
    with readonly_db_session() as session:
        row = (session.query(PlatformUserProfileModel)
                .filter(PlatformUserProfileModel.user_id == useId).first())
        ret = row
        return ret


def insertUserBaseInfo(entity: PlatformUserModel):
    with auto_db_session() as session:
        session.add(entity)
        return entity.user_id


def setUserRole(user_id, role:int):
    with auto_db_session() as session:
        stmt = update(PlatformUserModel).where(PlatformUserModel.user_id == user_id).values(role=role)
        session.execute(stmt)


def updateUserProfilesAndRole(user_profile: PlatformUserProfileModel,role:str):
    with auto_db_session() as session:
        row = session.query(PlatformUserProfileModel).filter(PlatformUserProfileModel.user_id == user_profile.user_id).first()
        if row is None:
            user_profile.created_at = user_profile.updated_at
            session.add(user_profile)
        else:
            stmt = update(PlatformUserProfileModel).where(PlatformUserProfileModel.user_id == user_profile.user_id).values(
                display_name = user_profile.display_name,
                city = user_profile.city,
                bio = user_profile.bio,
                industry_tags = user_profile.industry_tags,
                skill_tags = user_profile.skill_tags,
                project_name = user_profile.project_name,
                project_stage = user_profile.project_stage,
                funding_stage = user_profile.funding_stage,
                need_tags = user_profile.need_tags,
                investment_tags = user_profile.investment_tags,
                team_size = user_profile.team_size,
                work_type = user_profile.work_type,
                title=user_profile.title,
                avatar_url = user_profile.avatar_url
            )
            session.execute(stmt)

        stmt = update(PlatformUserModel).where(PlatformUserModel.user_id == user_profile.user_id).values(role=role)
        session.execute(stmt)

def updateLastActiveDatetime(user_id):
    with auto_db_session() as session:
        stmt =update(PlatformUserModel).where(PlatformUserModel.user_id == user_id).values(last_active = datetime.now())
        session.execute(stmt)


def updateProfileCompleteness(user_id,completeness:int):
    with auto_db_session() as session:
        stmt = update(PlatformUserProfileModel).where(PlatformUserProfileModel.user_id == user_id).values(completeness=completeness)
        session.execute(stmt)

def getProfileCompleteness(userId):
    with readonly_db_session() as session:
        row = (session.query(PlatformUserProfileModel.completeness).filter(PlatformUserProfileModel.user_id==userId)).first()
        completeness = row.completeness
        return completeness


def getUserTokenCount(userId):
    with readonly_db_session() as session:
        row = (session.query(PlatformUserModel.token_count).filter(PlatformUserProfileModel.user_id==userId)).first()
        token_count = row.token_count
        return token_count

def updateTokenCount(user_id,action:str,canAward:int,metadata=None):
    with auto_db_session() as session:
        session.query(PlatformUserModel).where(PlatformUserModel.user_id == user_id).update({PlatformUserModel.token_count:PlatformUserModel.token_count+canAward})

        log = PlatformTokenLogModel()
        log.action = action
        log.user_id = user_id
        log.amount = canAward
        log.meta_data = metadata

        session.add(log)

def getTokenLogByAction(user_id,action):
    with readonly_db_session() as session:
        query = session.query(PlatformTokenLogModel).filter(PlatformTokenLogModel.user_id == user_id and PlatformTokenLogModel.action == action).order_by(PlatformTokenLogModel.id.desc())
        row = (query.first())
        if row is None:
            return 0
        else:
            amount = row.amount
            return amount

def updatePassword(user_id, password):
    with auto_db_session() as session:
        session.query(PlatformUserModel).where(PlatformUserModel.user_id == user_id).update({PlatformUserModel.password:password})


