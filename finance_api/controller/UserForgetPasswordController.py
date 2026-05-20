# -*- coding: utf-8 -*-
import os
import random
from flask import Blueprint, request
from common import RedisKey
from common.Email import EmailClient
from common.Logger import getLogger
from common.Redis import RedisClient
from common.Response import ResponseDTO
from common.utilities import SecurityUtils
from database.common import PlatformUserManager
from database.dao import PlatformUserDao, PlatformUserAuthLogDao

forgetPassword = Blueprint("forgetPassword", __name__,url_prefix="/api/user")
userDao = PlatformUserDao
logger = getLogger(os.path.basename(__file__))
userAuthLogDao = PlatformUserAuthLogDao

@forgetPassword.post("/forgetPassword/send_code_by_email")
def send_code_by_email():
    json_body = request.get_json()
    if not json_body or not isinstance(json_body, dict):
        return ResponseDTO().error('数据为空或格式不对').toJson()
    email = json_body.get("email")

    result = userDao.findByEmail(email)
    if result is None:
        return ResponseDTO().error("邮件不存在").toJson()
    else:
        try:
            code = random.randint(10000, 99999)

            redis = RedisClient()
            key = RedisKey.REDIS_KEY_USER_FORGET_PASSWORD % email

            redis.setex(key,code,60)

            emailClient = EmailClient()
            emailClient.send_verification_code(email,code)

            return ResponseDTO().ok().toJson()
        except Exception as e:
            logger.error(f"{str(e)}", exc_info=True)
            return ResponseDTO().error(e.args[0]).toJson()


@forgetPassword.post("/forgetPassword/send_code_by_phone")
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
            key = RedisKey.REDIS_KEY_USER_FORGET_PASSWORD % phone
            redis.set(key,code,60)

            return ResponseDTO().ok().toJson()
        except Exception as e:
            logger.error(f"str{e}", exc_info=True)
            return ResponseDTO().error(e.args[0]).toJson()

@forgetPassword.route("/forgetPassword/doResetPassword", methods=["POST"])
def doResetPassword():
    request_data = request.get_json()
    userAgent = request.user_agent.string
    userId = request_data['userId']

    password = request_data["password"]
    confirmPassword = request_data["confirmPassword"]

    if password == '' or password is None:
        return ResponseDTO().error("密码不能为空!").toJson()
    elif password!=confirmPassword:
        return ResponseDTO().error("两次输入的密码不一致!").toJson()

    rd = userDao.findById(userId)
    if rd is None :
        return ResponseDTO().error("用户不存在!").toJson()


    try:
        userDao.updatePassword(userId,SecurityUtils.encryption(password))
        userAuthLogDao.insertUserAuthLog(userId,PlatformUserManager.AuthAuthActionEnum.value, userAgent, True)

        return ResponseDTO().ok().setMessage("密码修改成功！").toJson()
    except Exception as e:
        logger.error(f"{str(e)}", exc_info=True)
        userAuthLogDao.insertUserAuthLog(userId, PlatformUserManager.AuthAuthActionEnum.value,  userAgent,False)
        return ResponseDTO().error(e.args[0]).toJson()


@forgetPassword.get("/forgetPassword/doConfirmPhoneOrMail")
def doConfirmPhoneOrMail():
    request_data = request.args
    phoneOrEmail = request_data.get('phoneOrEmail')
    verificationCode = request_data.get("verificationCode")

    key = RedisKey.REDIS_KEY_USER_FORGET_PASSWORD % phoneOrEmail
    redis = RedisClient()
    v = redis.get(key)
    if v != verificationCode:
        return ResponseDTO().error("验证码不正确！").toJson()

    if phoneOrEmail is None or phoneOrEmail =='':
        return ResponseDTO().error("手机号或邮箱不能为空！").toJson()

    result = userDao.findByEmailOrPhone(phoneOrEmail)
    if result is None:
        return ResponseDTO().error("手机号或邮箱不存在").toJson()
    return ResponseDTO().ok().setData({'userId': str(result.user_id)}).setMessage("验证码正确，请修改密码").toJson()