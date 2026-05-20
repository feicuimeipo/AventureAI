import datetime
from datetime import timedelta

from django.contrib.admin import actions
from elasticsearch.esql.functions import first
from sqlalchemy import and_, select, desc
from sqlalchemy.orm import aliased
from common.utilities.NetUtils import get_real_client_ip
from database.common import PlatformUserManager
from database.db_conn import auto_db_session, readonly_db_session
from database.entity.PlatformUserAuthLog import PlatformUserAuthLogModel
from database.entity.PlatformUserProfile import PlatformUserProfileModel


def insertUserAuthLog(userId, action, userAgent, success: bool):
    with auto_db_session() as session:
        entity = PlatformUserAuthLogModel()
        entity.user_id = userId
        entity.action = action
        entity.ip_addr = get_real_client_ip()
        entity.success = success
        entity.create_at = datetime.datetime.now()
        entity.user_agent = userAgent
        session.add(entity)


def insertUserAuthLog_Login(userId, userAgent, success: bool):
    AuthLog = aliased(PlatformUserAuthLogModel, name='log')
    with auto_db_session() as session:
        # row = session.query(AuthLog).filter(
        #     and_(AuthLog.user_id = userId, AuthLog.action == "login", AuthLog.is_first_login == True).first()

        entity = PlatformUserAuthLogModel()
        entity.user_id = userId
        entity.action = "login"
        entity.ip_addr = get_real_client_ip()
        entity.success = bool
        entity.create_at = datetime.datetime.now()
        entity.user_agent = userAgent
        session.add(entity)
