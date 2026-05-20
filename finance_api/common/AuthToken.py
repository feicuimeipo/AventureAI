import datetime
import functools
import os
import secrets

import jwt
from flask import request, jsonify

from app.config import EnvConfig
from common import RedisKey
from common.Exception import AccessTokenLogoutException
from common.Logger import getLogger
from common.Redis import RedisClient
from common.Response import ResponseDTO

JWT_TOKEN_EXPIRE:int = 3600 * 24
Algorithm = 'HS256'
logger = getLogger((os.path.basename(__file__)))

def generateAccessToken(user_id):
    # 创建 JWT 令牌
    payload = {
        'user_id':str(user_id),  # 示例用户ID，应替换为实际用户ID
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=JWT_TOKEN_EXPIRE),  # 设置过期时间
        'iat': datetime.datetime.now(datetime.UTC)
    }

    secret_key = EnvConfig.JWT_SECRET_KEY
    if len(secret_key)<32:
        secret_key = secrets.token_bytes(32)  # 生成安全的 32 字节密钥

    #base64_secret =base64.b64decode(secret_key)
    accessToken = jwt.encode(payload, secret_key, algorithm=Algorithm)

    token = accessToken

    return token


def getAccessTokenFromRequest(req):
    token = None
    if 'Authorization' in req.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]
    return token


# 装饭器
def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = getAccessTokenFromRequest(request)
        if not token:
            return jsonify({'message': 'Token已丢失!'}), 401
        try:
            redis = RedisClient()
            # 检查Token是否在Redis黑名单中（用于登出）
            if redis and redis.exists(f"blacklist:{token}"):
                return jsonify({'message': 'Token已被登录(撤消)'}), 401

            # 解码Token
            data = jwt.decode(token, EnvConfig.JWT_SECRET_KEY, algorithms=Algorithm)
            current_user = data['user_id']
        except jwt.ExpiredSignatureError as e:
            logger.error(e,exc_info=True)
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            logger.error(e, exc_info=True)
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


def getUserIdFromToken(accessToken):
    secret_key = EnvConfig.JWT_SECRET_KEY
    try:
        decoded = jwt.decode(accessToken, secret_key, algorithms=['HS256'])
        uid = decoded['user_id']  # 返回 user_id 或其他相关信息
        if uid:
            return uid
        else:
            logger.info('header.Authorization中的文户与redis中的用户不一致！')
            return None
    except jwt.ExpiredSignatureError as e:
        logger.info(f'Token过期：{e}')
        return None
    except jwt.InvalidTokenError as e:
        logger.info(f'Token无效：{e}')
        return None


# 验证用户是否登录
def verifyAccessToken(req) -> str | None:
    accessToken = getAccessTokenFromRequest(req)
    redis = RedisClient()

    # 检查Token是否在Redis黑名单中（用于登出）
    if redis and redis.exists(f"blacklist:{accessToken}"):
        logger.error('用户已退出！')
        return None

    key = RedisKey.REDIS_KEY_AUTH_TOKEN % accessToken
    user_id = redis.get(key)  # 从 Redis 获取 user_id
    secret_key = EnvConfig.JWT_SECRET_KEY
    if user_id:
        try:
            decoded = jwt.decode(accessToken, secret_key, algorithms=['HS256'])
            uid = decoded['user_id']  # 返回 user_id 或其他相关信息
            if user_id==uid:
                return uid
            else:
                logger.info('header.Authorization中的文户与redis中的用户不一致！')
                return None
        except jwt.ExpiredSignatureError as e:
            logger.info(f'Token过期：{e}')
            return None
        except jwt.InvalidTokenError as e:
            logger.info(f'Token无效：{e}')
            return None
    else:
        return None


def authTokenLogout(req):
    token = getAccessTokenFromRequest(req)
    redis = RedisClient()
    if token and redis:
        try:
            decoded = jwt.decode(token, EnvConfig.JWT_SECRET_KEY, algorithms=[Algorithm], options={"verify_exp": False})
            # jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
            exp_timestamp = decoded.get('exp')
            if exp_timestamp:
                ttl = exp_timestamp - int(datetime.datetime.now('UTC').timestamp())
                if ttl > 0:
                    redis.setex(f"blacklist:{token}", "revoked", ttl)
        except Exception as e:
            logger.error(e, exc_info=True)
            return ResponseDTO().error(e.args[0]).toJson()
    return ResponseDTO().ok().setMessage("登出成功").toJson()

