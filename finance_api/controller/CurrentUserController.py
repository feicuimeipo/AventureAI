# -*- coding: utf-8 -*-
import json
import os

from flask import Blueprint, request
from _schedule.task_user_profile import record_user_stat
from common import RedisKey, AuthToken
from common.AuthToken import getAccessTokenFromRequest
from common.Logger import getLogger
from common.Redis import RedisClient
from common.Response import ResponseDTO
from database.common import UserStatManager
from database.dao import PlatformUserDao, PlatformUserAuthLogDao, PlatformUserStatDao, PlatformCeleryTaskLogDao

# 实例化一个蓝图对象
currentUser = Blueprint("currentUser", __name__,url_prefix="/api/user")
userDao = PlatformUserDao
usrAuthLogDao = PlatformUserAuthLogDao
logger = getLogger(os.path.basename(__file__))

@currentUser.route("/currentUser/info")
def getCurrentInfo():
    uid = AuthToken.verifyAccessToken(request)
    if not uid:
        return ResponseDTO().error("用户未登录").toJson()

    redis = RedisClient()
    key = RedisKey.REDIS_KEY_USER_DETAIL % uid
    dataStr = redis.get(key)
    if dataStr:
        data = json.loads(dataStr)
        return ResponseDTO().ok().setData(data).toJson()
    else:
        detail = userDao.getDetailById(uid)
        if not detail:
            return ResponseDTO().error('用户不存在').setCode(404).toJson()
        data = {
            'userId': str(detail.u.user_id),
            'email': detail.u.email,
            "phone": detail.u.phone if detail.__contains__('phone') else "",
            'role': detail.u.role,
            'city': detail.p.city,
            'displayName': detail.p.display_name,
            'industryTags': detail.p.industry_tags,
            'skillTags': detail.p.skill_tags,
            'projectName': detail.p.project_name,
            'projectStage': detail.p.project_stage,
            'fundingStage': detail.p.funding_stage,
            'needTags': detail.p.need_tags,
            'teamSize': detail.p.team_size,
            'investmentTags': detail.p.investment_tags,
            "title": detail.p.title,
            'workType': detail.p.work_type,
        }
        redis.set(key, json.dumps(data), ex=AuthToken.JWT_TOKEN_EXPIRE)
        redis.expire(key,60)
        return ResponseDTO().ok().setData(data).toJson()


@currentUser.get("/currentUser/getCompleteness")
def getCompleteness():
    completeness = 0
    userId = AuthToken.verifyAccessToken(request)
    if userId:
        redis = RedisClient()
        key = RedisKey.getUserCompletenessKey(userId)
        completeness = redis.get(key)
        if not completeness:
            completeness = userDao.getProfileCompleteness(userId)
            redis.set(key,completeness)
    return ResponseDTO().ok().setData({"completeness": completeness}).toJson()

@currentUser.get("/currentUser/getAwardTokens")
def getAwardTokens():
    token_count = 0
    redis = RedisClient()
    userId = AuthToken.verifyAccessToken(request)
    if userId:
        key = RedisKey.getUserTokenCountKey(userId)
        token_count = redis.get(key)
        if token_count:
            token_count = userDao.getUserTokenCount(userId)
            redis.set(key,token_count)
    return ResponseDTO().ok().setData({"tokenCount": token_count}).toJson()

@currentUser.get("/currentUser/loginState")
def loginState():
    uid = AuthToken.verifyAccessToken(request)
    if uid:
        return ResponseDTO().ok().setData({"loginState":'true','userId':uid}).toJson()
    else:
        logger.info("用户未登录")
        return ResponseDTO().error("用户未登录").setData({"loginState": 'false', 'userId': uid}).toJson()

@currentUser.get("/currentUser/refreshToken")
def refreshUseActive():
    accessToken = getAccessTokenFromRequest(request)
    uid = AuthToken.verifyAccessToken(request)
    if uid:
        redis = RedisClient()
        key = RedisKey.REDIS_KEY_AUTH_TOKEN % accessToken
        redis.setExpire(key,AuthToken.JWT_TOKEN_EXPIRE)
        userDao.updateLastActiveDatetime(uid)
    return ResponseDTO().ok().toJson()


@currentUser.post("/currentUser/stat/behaviorLog")
def updateUserLastActivity():
    datas = request.get_json()
    for data in datas:
        try:
            authToken = data["authToken"]
            userId = AuthToken.getUserIdFromToken(authToken)
            if userId:
                duration = data["duration"]
                timestamp = data["lastActiveTime"]
                duration = min((duration / 1000), 60) if duration else 0
                UserStatManager.calculate_activity_duration(userId,int(duration))
                UserStatManager.calculate_last_activity_time(userId,timestamp)
                UserStatManager.calculate_user_browse_count(userId)
                UserStatManager.calculate_daily_login_count(userId)
                userDao.updateLastActiveDatetime(userId)

                # 发送定时任务
                celery_task_result = record_user_stat.apply_async(
                    args=[],
                    countdown=5  # 倒计时 10 秒后执行
                )
                PlatformCeleryTaskLogDao.insertCeleryLog(celery_task_result.id, 'record_user_stat', 'start_up')

        except Exception as e:
            logger.error(e,exc_info=True)
    return ResponseDTO().ok().toJson()

@currentUser.post("/currentUser/stat/message_count")
def updateUserBrowseCount():
    userStateDao = PlatformUserStatDao
    uid = AuthToken.verifyAccessToken(request)
    if uid:
        UserStatManager.calculate_message_count(uid)
    return ResponseDTO().ok().toJson()



