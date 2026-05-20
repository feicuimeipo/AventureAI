# -*- coding: utf-8 -*-
import os
import uuid
from datetime import timedelta, datetime
from _schedule.task_partner_match import partner_match_based_on_need
from flask import Blueprint, request
from common import AuthToken
from common.Exception import AccessTokenLogoutException
from common.Logger import getLogger
from common.Response import ResponseDTO
from database.common import PlatformUserManager, UserStatManager
from database.common.PlatformUserManager import AwardTokenRuleEnum
from database.dao import PlatformNeedDao, PlatformCeleryTaskLogDao
from database.entity.PlatformCofounderNeed import PlatformCofounderNeedModel

needBt = Blueprint("needBt", __name__,url_prefix="/api/needs")
logger = getLogger(os.path.basename(__file__))
needDao = PlatformNeedDao

@needBt.post("/post")
def postNeeds():
    try:
        need = PlatformCofounderNeedModel()
        uid = AuthToken.verifyAccessToken(request)
        if uid:
            need.user_id = uuid.UUID(uid)
        else:
            return ResponseDTO().error("用户未登录，请选登录").toJson()

        request_data = request.get_json()
        need.id = uuid.uuid4()
        need.title = request_data["title"]
        need.role_wanted = request_data["roleWanted"]
        need.work_type = request_data["workType"]
        need.description = request_data["description"]
        need.industry = request_data["industry"]
        need.equity_range = request_data["equityRange"]
        need.status = 'active'
        now = datetime.now()
        need.created_at = now
        need.update_at = now
        need.expired_at = now + timedelta(days=90)
        need.skill_reqs = request_data["skillReqs"].split(",") if request_data["skillReqs"] else None
        need.city_reqs = request_data["cityReqs"].split(",") if request_data["cityReqs"] else None

        needDao.insertNeed(need)

        # 发送定时任务
        # celery_task_result = celery_tasks_user_profile.transform_user_profile_into_milvus.delay(userProfile.user_id)
        celery_task_result = partner_match_based_on_need.apply_async(
            args=[need.id],
            countdown=5
        )
        PlatformCeleryTaskLogDao.insertCeleryLog(celery_task_result.id, 'partner_match_based_on_need', celery_task_result.status)
        PlatformUserManager.calcAwardTokenByRule(uid, AwardTokenRuleEnum.PublishNeed.name)
        UserStatManager.calculate_activity_duration(uid, 60)

        return ResponseDTO().ok().setData({"id":str(need.id)}).toJson()
    except AccessTokenLogoutException as a:
        return ResponseDTO().error("用户未登录，请选登录").toJson()
    except Exception as e:
        logger.error(e)
        return ResponseDTO().error(e).toJson()


@needBt.get("/list")
def getList():
    try:
        uid = AuthToken.verifyAccessToken(request)
        if uid:
            dataList = needDao.getDataLists(uid)

            rets = []
            for row in dataList:
                data = {
                    "id": str(row.id),
                    "user_id": str(row.user_id),
                    "title": row.title,
                    "description": row.description,
                    "role_wanted": row.role_wanted,
                    "work_type": row.work_type,
                    "industry": row.industry,
                    "equity_range": row.equity_range,
                    "vesting": row.vesting,
                    "status": row.status,
                    "view_count": row.view_count,
                    "created_at": str(row.created_at),
                    "expired_at": str(row.expired_at),
                    "embedding_update_at": str(row.embedding_update_at),
                    "update_at": str(row.update_at),
                    "skill_reqs": row.skill_reqs,
                    "city_reqs": row.city_reqs,
                    "match_update_at": str(row.match_update_at)
                }
                rets.append(data)

            return ResponseDTO().ok().setData(rets).toJson()
        else:
            return ResponseDTO().error("用户未登录，请选登录").toJson()

    except AccessTokenLogoutException:
        return ResponseDTO().error("用户未登录，请选登录").toJson()
    except Exception as e:
        logger.error(e)
        return ResponseDTO().error(f'{str(e)}').toJson()


@needBt.get("/detail")
def getDetail():
    try:
        uid = AuthToken.verifyAccessToken(request)
        if uid:
            idStr = request.args.get('id', default='', type=str)
            if idStr is None or idStr == '':
                return ResponseDTO().error("需求编号不可以为空！").toJson()

            row = needDao.getById(idStr)

            return ResponseDTO().ok().setData(ret).toJson()
        else:
            return ResponseDTO().error("用户未登录，请选登录").toJson()

    except AccessTokenLogoutException:
        return ResponseDTO().error("用户未登录，请选登录").toJson()
    except Exception as e:
        logger.error(e, exc_info=True)
        return ResponseDTO().error(str(e)).toJson()


@needBt.post("/edit")
def doModifyNeed():
    try:
        need = PlatformCofounderNeedModel()

        uid = AuthToken.verifyAccessToken(request)
        if uid:
            need.user_id = uuid.UUID(uid)
        else:
            return ResponseDTO().error("用户未登录，请选登录").toJson()

        request_data = request.get_json()
        if 'id' not in request_data or request_data['id'] is None:
            return ResponseDTO().error("需求编码不可以为空！").toJson()

        need.id = uuid.UUID(request_data["id"])
        need.title = request_data["title"]
        need.role_wanted = request_data["roleWanted"]
        need.work_type = request_data["workType"]
        need.description = request_data["description"]
        need.industry = request_data["industry"]
        need.equity_range = request_data["equityRange"]
        need.status = request_data["status"]
        need.skill_reqs = request_data["skillReqs"].split(",") if request_data["skillReqs"] else None
        need.city_reqs = request_data["cityReqs"].split(",") if request_data["cityReqs"] else None
        need.update_at = datetime.now()

        needDao.updateNeed(need)

        # 发送定时任务
        celery_task_result = partner_match_based_on_need.apply_async(
            args=[need.id],
            countdown=5  # 倒计时 10 秒后执行
        )
        PlatformCeleryTaskLogDao.insertCeleryLog(celery_task_result.id, 'partner_match_based_on_need', 'start_up')

        return ResponseDTO().ok().toJson()
    except AccessTokenLogoutException:
        return ResponseDTO().error("用户未登录，请选登录").toJson()
    except Exception as e:
        logger.error(e, exc_info=True)
        return ResponseDTO().error(str(e)).toJson()