# -*- coding: utf-8 -*-
import json
import os
import uuid
from datetime import timedelta, datetime

from django.conf.locale import fa
from flask import Blueprint, request

from common import RedisKey, AuthToken
from common.Logger import getLogger
from common.Redis import RedisClient
from common.Response import ResponseDTO
from database.dao import PlatformMatchResultDao, PlatformMatchInteractionDao, PlatformNeedDao
from database.entity.PlatformMatchInteractions import PlatformMatchInteractionModel

partnerMatchBP = Blueprint("partnerMatch", __name__,url_prefix="/api/partner")
logger = getLogger(os.path.basename(__file__))
matchResultsDao = PlatformMatchResultDao
interactionDao = PlatformMatchInteractionDao
needDao = PlatformNeedDao

@partnerMatchBP.get("/detail/<id>")
def getCandidateDetail(id):
    try:
        redisClient = RedisClient()
        key = RedisKey.getMatchResultDetailKey(id)
        data = redisClient.get(key)
        if data:
            result = json.loads(data)
            return ResponseDTO().ok().setData(result).toJson()

        row = matchResultsDao.getCandidateDetail(id)
        result = {}
        if row:
            result["id"] = str(row.s.id)
            result["seekerId"] = str(row.s.seeker_id)
            result["candidateId"] = str(row.s.candidate_id)
            result["role"] = row.u.role

            result["needId"] = str(row.s.need_id)
            result["scoreTotal"] = str(row.s.score_total)
            result["scoreDetail"] = row.s.score_detail
            result["reasons"] = row.s.reasons
            result["isFeatured"] = row.s.is_featured
            result["featureDesc"] = '今日精选 ✦' if row.s.is_featured else ''  # 精选
            result["needIndustryReq"] = row.c.industry

            result["displayName"] = row.p.display_name if row.p.display_name else ' '
            result["bio"] = row.p.bio
            result["city"] = row.p.city
            result["skillTags"] = row.p.skill_tags
            result["industryTags"] = row.p.industry_tags
            result["completeness"] = row.p.completeness
            result["teamSize"] = row.p.team_size
            result["needTags"] = row.p.need_tags
            result["title"] = row.p.title
            result["workType"] = row.p.work_type
            result["projectName"] = row.p.project_name
            result["projectStage"] = row.p.project_stage
            result["fundingStage"] = row.p.funding_stage
            result["investmentTags"] = row.p.investment_tags
            result["profileData"] = row.p.profile_data

            # try:
            if row.u.last_active:
                today = datetime.today()
                yesterday = today - timedelta(days=1)
                beforeYesterday = today - timedelta(days=2)

                activeTime = row.u.last_active
                if activeTime.date() == today.date():
                    result["lastActiveTimeDesc"] = f'今天 {activeTime.time()} 在线'
                elif activeTime.date() == yesterday.date():
                    result["lastActiveTimeDesc"] = f'昨天 {activeTime.time()} 在线'
                elif activeTime.date() == beforeYesterday.date():
                    result["lastActiveTimeDesc"] = f'前天 {activeTime.time()} 在线'
                else:
                    result["lastActiveTimeDesc"] = f'{today - activeTime.date()}天前 {activeTime.hour}时 在线'
                # result["lastActiveTime"] = activeTime;
            # except Exception as e:
            #     logger.error(str(e))

            interactions = interactionDao.listInteractionAction(str(row.s.seeker_id), str(row.s.candidate_id), row.s.id)
            actions = []
            for item in interactions:
                actions.append(item.action)
            result["isInterest"] = ("interest" in actions)
            result["isMutual"] = ("mutual" in actions)
            result["isSkip"] = ("skip" in actions)
            result["isFavorite"] = ("favorite" in actions)
            result["isBlock"] = ("block" in actions)

            redisClient.set(key, json.dumps(result))
            redisClient.expire(key, 60)

            scoreKey = RedisKey.getMatchResultScoreKey(id)
            redisClient.set(scoreKey, json.dumps(row.s.score_detail))

        return ResponseDTO().ok().setData(result).toJson()
    except Exception as e:
        logger.error(str(e))
        return ResponseDTO().error(f"{str(e)}").toJson()

@partnerMatchBP.get("/matchScore/<id>")
def getMatchScoreDetail(id):
    if not id or id=='undefined':
        return ResponseDTO().error("id为空").toJson()

    try:
        redisClient = RedisClient()
        scoreKey = RedisKey.getMatchResultScoreKey(id)
        detail = redisClient.get(scoreKey)
        if detail:
            detail = json.loads(detail)
            return ResponseDTO().ok().setData(detail).toJson()
        else:
            detail = matchResultsDao.getCandidateMatchScoreDetail(id)
            if detail:
                redisClient.set(scoreKey, json.dumps(detail))
                redisClient.expire(scoreKey, 60)
                return ResponseDTO().ok().setData(detail).toJson()
        return ResponseDTO().error("未找到记录").setCode(404).toJson()
    except Exception as e:
        logger.error(str(e))
        return ResponseDTO().error(str(e)).toJson()


@partnerMatchBP.post("/addAction")
def addAction():
    request_data = request.get_json()

    from_user_id = request_data["from_user_id"]
    to_user_id = request_data["to_user_id"]
    result_id = request_data["result_id"]
    need_id = request_data["need_id"]
    action = request_data.get("action")
    message = request_data.get["message"]
    interactionType = request_data.get["interactionType"]
    if not interactionType:
        return ResponseDTO().error("意向类型不能为空！").setCode(501).toJson()
    if need_id:
        need = needDao.getById(need_id)
        if not need:
            return ResponseDTO().error("搭子匹配的需求不能为空！").setCode(501).toJson()
    if action == 'interest' and not message:
        return ResponseDTO().error("消息为能为空！").setCode(501).toJson()

    matchInteraction = PlatformMatchInteractionModel()
    matchInteraction.from_user_id = from_user_id
    matchInteraction.to_user_id = to_user_id
    matchInteraction.is_mutual = False
    matchInteraction.created_at = datetime.now()
    matchInteraction.result_id = result_id
    matchInteraction.need_id = need_id
    matchInteraction.type = interactionType

    matchInteraction.id = uuid.uuid4()
    matchInteraction.action = action
    matchInteraction.is_mutual = False
    matchInteraction.created_at = datetime.now()
    interactionDao.addMatchInteraction(matchInteraction)

    redisClient = RedisClient()
    key = RedisKey.getInteractionListKey(from_user_id, to_user_id, result_id)
    redisClient.delete(key)
    return ResponseDTO().ok().toJson()

@partnerMatchBP.post("/cancelAction")
def cancelAction():
    request_data = request.get_json()
    from_user_id = request_data["from_user_id"]
    to_user_id = request_data["to_user_id"]
    result_id = request_data["result_id"]
    action = request_data.get("action")

    interactionDao.deleteMatchInteraction(from_user_id,to_user_id, result_id, action)

    redisClient = RedisClient()
    key = RedisKey.getInteractionListKey(from_user_id, to_user_id, result_id)
    redisClient.delete(key)
    return ResponseDTO().ok().toJson()


def isAction(from_user_id, to_user_id, result_id, action):
    redisClient = RedisClient()
    key = RedisKey.getInteractionListKey(from_user_id, to_user_id, result_id)
    data = redisClient.get(key)
    interactions = json.loads(data) if data else []
    if not interactions:
        interactions = interactionDao.listInteractionAction(from_user_id, to_user_id, result_id)
        redisClient.set(key, json.dumps(interactions))

    for row in interactions:
        if action == 'mutual' and row.is_mutual:
            return True
        elif action == row.action:
            return True
    return False



@partnerMatchBP.get("/list")
def findPartner():
    currentUid = AuthToken.verifyAccessToken(request)
    if not currentUid:
        return ResponseDTO().error("请先登录").setCode(404).toJson()

    request_data = request.args
    needId = request_data.get("needId", default=None, type=str)
    myCandidateType = request_data.get("myCandidateType", default=None, type=str)
    if not needId and not myCandidateType:
        return ResponseDTO().error("请先选择一个需求或搭子类型").setCode(404).toJson()



    page = request_data.get("page", default=1, type=int)
    per_page = request_data.get("per_page", default=10, type=int)
    params = {
        "myCandidateType": myCandidateType,
        "rangeValue": request_data.get("rangeValue", default=None, type=int),
        "orderBy": request_data.get("orderBy", default="score", type=str),
        "currentUid": currentUid,
    }
    results = []
    rows, total = matchResultsDao.findMatchResult(needId, params, int(page), int(per_page))

    if total<=0:
       return ResponseDTO().error("AI正在努力计算中...！").setCode(405).toJson()

    is_last_page = True if (per_page * page + per_page) >= total else False
    for row in rows:
        vo = {}
        vo["id"] = str(row.s.id)
        vo["needId"] = str(row.s.need_id)
        vo["seekId"] = str(row.s.seeker_id)
        vo["candidateId"] = str(row.s.candidate_id)

        vo["displayName"] = row.p.display_name if row.p.display_name else ' '
        vo["role"] = str(row.u.role)
        vo["city"] = row.p.city
        vo["title"] = row.p.title
        vo["bio"] = row.p.bio
        vo["skillTags"] = row.p.skill_tags
        vo["industryTags"] = row.p.industry_tags
        vo["reasons"] = row.s.reasons
        vo["scoreTotal"] = str(row.s.score_total)
        vo["scoreDetail"] = row.s.score_detail
        vo["isFeature"] = row.s.is_featured
        vo["feature"] = 'match-card feature'  if row.s.is_featured else 'match-card' #精选

        interactions = interactionDao.listInteractionAction(str(row.s.seeker_id), str(row.s.candidate_id), row.s.id)
        actions = []
        for item in interactions:
            actions.append(item.action)
        vo["isInterest"] = ("interest" in actions)
        vo["isMutual"] = ("mutual" in actions)
        vo["isSkip"] = ("skip" in actions)
        vo["isFavorite"] = ("favorite" in actions)
        vo["isBlock"] = ("block" in actions)

        results.append(vo)

    return ResponseDTO().ok().setData({"list": results,
                                       'page': page,
                                       'perPage':per_page,
                                       'isLastPage': is_last_page,
                                       'total': total}).toJson()




