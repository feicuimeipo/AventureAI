# -*- coding: utf-8 -*-
import datetime
import os
import random
import uuid

from flask import Blueprint, request

from _schedule.task_user_profile import transform_user_profile_into_milvus
from common import RedisKey
from common.Email import EmailClient
from common.Logger import getLogger
from common.Redis import RedisClient
from common.Response import ResponseDTO
from common.utilities import SecurityUtils
from database.common import PlatformUserManager
from database.dao import PlatformUserDao, PlatformUserAuthLogDao, PlatformCeleryTaskLogDao
from database.entity.PlatformUser import PlatformUserModel
from database.entity.PlatformUserProfile import PlatformUserProfileModel

userRegister = Blueprint("userRegister", __name__,url_prefix="/api/user/register")
logger = getLogger(os.path.basename(__file__))
userManager = PlatformUserManager
userDao = PlatformUserDao
userAuthLogDao = PlatformUserAuthLogDao

@userRegister.post("/send_code_by_email")
def send_code_by_email():

    json_body = request.get_json()
    if not json_body or not isinstance(json_body, dict):
        return ResponseDTO().error('数据为空或格式不对').toJson()
    email = json_body.get("email")

    result = userDao.findByEmail(email)
    if result is not None:
        return ResponseDTO().error("邮件已经存在").toJson()
    else:
        try:
            code = random.randint(10000, 99999)

            redis = RedisClient()
            key = RedisKey.REDIS_KEY_USER_REGISTER % email

            redis.set(key,code,ex=60)

            emailClient = EmailClient()
            emailClient.send_verification_code(email,code)

            return ResponseDTO().ok().toJson()
        except Exception as e:
            logger.error("{e}", exc_info=True)
            return ResponseDTO().error(e.args[0]).toJson()


@userRegister.post("/send_code_by_phone")
def send_code_by_phone():
    json_body = request.get_json()
    if not json_body or not isinstance(json_body, dict):
        return ResponseDTO().error('数据为空或格式不对').toJson()

    phone = json_body.get("phone")
    result = userDao.findByPhone(phone)
    if result is not None:
        return ResponseDTO().error("手机已经存在").toJson()
    else:
        try:
            code = random.randint(10000, 99999)

            redis = RedisClient()
            key = RedisKey.REDIS_KEY_USER_REGISTER % phone
            redis.set(key,code,ex=60)

            return ResponseDTO().ok().toJson()
        except Exception as e:
            logger.error("{e}", exc_info=True)
            return ResponseDTO().error(e.args[0]).toJson()



@userRegister.route("/do", methods=["POST"])
def register():
    request_data = request.get_json()
    phoneOrEmail = request_data['phoneOrEmail']
    verificationCode = request_data["verificationCode"]

    key = RedisKey.REDIS_KEY_USER_REGISTER % phoneOrEmail
    redis = RedisClient()
    v = redis.get(key)
    if v != verificationCode:
        return ResponseDTO().error("验证码不正确！").toJson()

    password = request_data["password"]
    confirmPassword = request_data["confirmPassword"]

    if password == '' or password is None:
        return ResponseDTO().error("密码不能为空!").toJson()
    elif password!=confirmPassword:
        return ResponseDTO().error("两次输入的密码不一致!").toJson()

    entity = PlatformUserModel()
    entity.password = SecurityUtils.encryption(password)
    try:
        result = userDao.findByEmailOrPhone(phoneOrEmail)
        if result is not None:
            return ResponseDTO().error("邮箱或手机号已存在").toJson()

        if str(phoneOrEmail).find("@"):
            entity.email = phoneOrEmail
        else:
            entity.phone = phoneOrEmail
        userId:uuid.UUID = uuid.uuid4()
        entity.user_id = userId
        entity.status = "active"
        entity.token_count = 0
        entity.is_verified = False
        entity.lang_pref = 'zh'
        entity.created_at = datetime.datetime.now(datetime.UTC)
        entity.updated_at = entity.created_at

        userDao.insertUserBaseInfo(entity)

        userAgent = request.user_agent.string
        userAuthLogDao.insertUserAuthLog(entity.user_id,
                                      userManager.AuthAuthActionEnum.REGISTER.value,
                                         userAgent,True)

        return ResponseDTO().ok().setData({'userId':str(userId)}).toJson()

    except Exception as e:
        logger.error(f"{e}", exc_info=True)
        return ResponseDTO().error(e.args[0]).toJson()


@userRegister.route("/doSaveRole", methods=["POST"])
def doSaveRole():
    try:
        request_data = request.get_json()
        userAgent = request.user_agent.string
        role = request_data['role']
        userId = request_data['userId']


        userDao.setUserRole(userId,role)
        userAuthLogDao.insertUserAuthLog(userId,
                                         userManager.AuthAuthActionEnum.UPDATE_ROLE.value,
                                         userAgent,True)

        return ResponseDTO().ok().setData({'role':role,'userId':userId}).toJson()
    except Exception as e:
        logger.error("{e}", exc_info=True)
        return ResponseDTO().error(e.args[0]).toJson()

@userRegister.post("/doSaveUserProfile")
def doSaveUserProfile():
    try:
        request_data = request.get_json()
        userAgent = request.user_agent.string
        userProfile = PlatformUserProfileModel()
        role = request_data['role']
        userId = request_data['userId']
        if userId:
            userProfile.user_id = uuid.UUID(userId)
        else:
            return ResponseDTO().error("userId不能为空")

        if 'avatarUrl' in request_data:
            userProfile.avatar_url = request_data['avatarUrl']
        else:
            userProfile.avatar_url = ''

        userProfile.display_name = request_data['displayName']
        userProfile.title = request_data['title']
        userProfile.bio = request_data['bio']
        userProfile.city = request_data['city']
        userProfile.skill_tags = request_data['skillTags'].split(",")
        userProfile.industry_tags  = request_data['industryTags'].split(",")
        userProfile.project_name = request_data['projectName']
        userProfile.project_stage = request_data['projectStage']
        userProfile.funding_stage = request_data['fundingStage']
        userProfile.team_size = request_data['teamSize']
        userProfile.need_tags = request_data['needTags'].split(",") if request_data['needTags'] else None
        userProfile.investment_tags = request_data['investmentTags'].split(",") if request_data['investmentTags'] else None
        userProfile.work_type = request_data['workType'].split(",") if request_data['workType'] else None
        userProfile.completeness = 0
        userProfile.tokenCount = 0
        userProfile.updated_at = datetime.datetime.now(datetime.UTC)
        userDao.updateUserProfilesAndRole(userProfile,role)

        redis = RedisClient()
        redis.delete(RedisKey.REDIS_KEY_USER_DETAIL % str(userProfile.user_id))

        # 发送定时任务
        try:
            celery_task_result =  transform_user_profile_into_milvus.apply_async(args=[userProfile.user_id], countdown=5.5, expires=120)
            PlatformCeleryTaskLogDao.insertCeleryLog(celery_task_result.id,'transform_user_profile_into_milvus', 'start_up')
        except Exception as e:
            logger.error(f"{str(e)}", exc_info=True)

        try:
            userManager.calcCompletenessAndToken(userProfile, role)
            userAuthLogDao.insertUserAuthLog(userId, userManager.AuthAuthActionEnum.UPDATE_PROFILE.value, userAgent, True)
        except Exception as e:
            logger.error(f"{str(e)}", exc_info=True)

        #奖励过的不会再奖
        return ResponseDTO().ok().toJson()
    except Exception as e:
        logger.error(f"{str(e)}", exc_info=True)
        return ResponseDTO().error(str(e)).toJson()



