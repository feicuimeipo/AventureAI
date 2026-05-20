import math
from datetime import datetime

from common import RedisKey
from common.Redis import RedisClient


def calculate_time_decay_score(update_timestamp, current_timestamp, decay_factor: float = 0.1) -> float:
    """
    计算档案更新时间的衰减得分
    公式: Score = Initial_Score * e^(-lambda * t)
    :param update_timestamp: 档案最后更新的时间戳(秒)
    :param current_timestamp: 当前时间戳(秒)
    :param decay_factor: 衰减系数 lambda，控制衰减速度
    :return: 衰减后的得分 (0-10分，假设初始满分为10)
    """
    update_date = datetime.strftime(update_timestamp,'%Y-%m-%d')
    current_date = datetime.strftime(current_timestamp,'%Y-%m-%d')
    if update_date >= current_date:
        return 10.0

    # 计算时间差（天）
    time_diff_days = (update_timestamp - current_timestamp) / (24 * 3600)
    if time_diff_days < 0: time_diff_days=0

    # 指数衰减计算
    initial_score = 10.0
    decayed_score = initial_score * math.exp( -decay_factor * time_diff_days)

    return decayed_score

def calculate_activity_duration(uid:str,duration:int):
    redisClient = RedisClient()
    key = RedisKey.getUserBehavior(uid)
    field = RedisKey.getUserBehavior_daily_duration_field()
    redisClient.hincrby(key, field, int(duration))
    #expire =  datetime.now() + timedelta(days=1)
    redisClient.expire(key, 3600 * 24)

def calculate_last_activity_time(uid,timestamp):
    redisClient = RedisClient()
    key = RedisKey.getUserBehavior(uid)
    field = RedisKey.getUserBehavior_last_activity_field()
    redisClient.hset(key, field, timestamp)
    redisClient.expire(key, 3600 * 24)

def calculate_user_browse_count(uid):
    redisClient = RedisClient()
    key = RedisKey.getUserBehavior(uid)
    field = RedisKey.getUserBehavior_browse_count_field()
    redisClient.hincrby(key, field,1)
    redisClient.expire(key, 3600 * 24)

def calculate_message_count(uid):
    redisClient = RedisClient()
    key = RedisKey.getUserBehavior(uid)
    field = RedisKey.getUserBehavior_message_count_field()
    redisClient.hincrby(key, field, 1)
    redisClient.expire(key, 3600 * 24 * 8)

def calculate_daily_login_count(uid):
    redisClient = RedisClient()
    key = RedisKey.getUserBehavior(uid)
    field = RedisKey.getUserBehavior_login_count_field()
    redisClient.hincrby(key, field, 1)
    redisClient.expire(key, 3600 * 24 * 8)
