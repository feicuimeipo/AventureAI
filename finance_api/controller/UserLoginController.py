# -*- coding: utf-8 -*-
import datetime
import os

from flask import Blueprint, request

from common import AuthToken, RedisKey
from common.Logger import getLogger
from common.Redis import RedisClient
# 实例化一个蓝图对象
from common.Response import ResponseDTO
from common.utilities import SecurityUtils
from database.common import PlatformUserManager, UserStatManager
from database.dao import PlatformUserDao, PlatformUserAuthLogDao

userLogin = Blueprint("userLogin", __name__,url_prefix="/api/user")
userDao = PlatformUserDao
userManager = PlatformUserManager
usrAuthLogDao = PlatformUserAuthLogDao
logger = getLogger(os.path.basename(__file__))

@userLogin.get("/doLogin")
def doLogin():
    pass

@userLogin.post("/doLoginByPassword")
def loginByPassword():

    try:
        request_data = request.get_json()
        phoneOrEmail = request_data["phoneOrEmail"]
        password = request_data["password"]
        userAgent = request.user_agent.string

        rd = userDao.findByEmailOrPhone(phoneOrEmail)
        if rd is None or rd.password != SecurityUtils.encryption(password):
            usrAuthLogDao.insertUserAuthLog_Login("-1", userAgent,False)
            raise Exception("用户或密码错误")

        # 创建Token，identity为用户ID
        accessToken =  AuthToken.generateAccessToken(rd.user_id)
        redis = RedisClient()
        key = RedisKey.REDIS_KEY_AUTH_TOKEN % accessToken
        redis.set(key, str(rd.user_id), ex=AuthToken.JWT_TOKEN_EXPIRE)

        try:
            UserStatManager.calculate_last_activity_time(rd.user_id, datetime.datetime.now().timestamp())
            userManager.calcAwardTokenByRule(rd.user_id, userManager.AwardTokenRuleEnum.DailyLogin)
            usrAuthLogDao.insertUserAuthLog_Login(rd.user_id,userAgent,True)
        except Exception as e:
            logger.error(e)

        logger.info("登录成功")
        return ResponseDTO().ok().setData({"accessToken":accessToken}).toJson()
    except Exception as e:
        logger.error(e)
        return ResponseDTO().error(f"用户或密码错误{str(e)}").toJson()

@userLogin.get("/doLogout")
def doLogout():
    try:
        uid = AuthToken.verifyAccessToken(request)
        if not uid:
            return ResponseDTO().error('用户已退出').toJson()
        else:
            return AuthToken.authTokenLogout(request)
    except Exception as e:
        logger.error(e)
        return ResponseDTO().error('用户已退出').toJson()


@userLogin.post("/loginByPhoneCode/send_code")
def loginByPhoneCode_sendCode():
   pass

@userLogin.post("/loginByPhoneCode/login")
def loginByPhoneCode_login():
   pass

