from datetime import datetime
from enum import Enum

from common import RedisKey
from common.Redis import RedisClient
from database.dao import PlatformUserDao
from database.dao.PlatformUserDao import updateProfileCompleteness
from database.entity.PlatformUserProfile import PlatformUserProfileModel


class UserRoleEnum(Enum):
  FOUNDER = "founder"
  INVESTOR = "investor"
  FA = "fa"
  EXPERT = "expert"
  CORP = "corp"
  GOV = "gov"

def getRoleDesc(role: str):
    if role == UserRoleEnum.FOUNDER.value:
        return '创业者'
    elif role == UserRoleEnum.INVESTOR.value:
        return '投资人'
    elif role == UserRoleEnum.FA.value:
        return '财务师'
    elif role == UserRoleEnum.EXPERT.value:
        return '行业专家'
    elif role == UserRoleEnum.CORP.value:
        return '企业方'
    elif role == UserRoleEnum.GOV.value:
        return '政府'
    return ''

class AuthAuthActionEnum(Enum):
    REGISTER = 'register'
    LOGIN = 'login'
    LOGOUT = 'logout'
    VERIFY = 'verify'
    RESET_PWD = 'reset_password'
    UPDATE_PROFILE = 'update_user_profile'
    UPDATE_ROLE= 'update_user_role'


"""颜档案完整度计算规则"""
class WeightEnum(Enum):
    display_name = 10
    bio = 20
    city = 5
    avatar_url = 5
    # profile_data = 30
    industry_tags = 15
    project_name = 10
    funding_stage = 10
    needTags = 10
    investment_stages=15
    skill_tags = 15



class AwardTokenRuleEnum(Enum):
    ProfileCompleteness = {
        'name':"filling_user_profile",
        'amount':100,
        'dailyLimit':100,
        'maxamount':1000,
    }
    DailyLogin = {
        'name':"dailyLogin",
        'amount':5,
        'dailyLimit':5
    },
    PublishNeed = {
        'name':"publish_need",
        'amount':5,
        'dailyLimit':5
    }
    EvaluateProject = {
        'name': "evaluate_project",
        'amount':100,
        'dailyLimit':100
    }
    InviteUser = {
        'name': "invite_user",
        'amount':30,
        'dailyLimit':9999
    }
    SuccessfulMatch = {
        'name':"successful_match",
        'amount':500,
        'dailyLimit':9999
    }



def calcTokenForRegister(user_id, completeness: int):
    userDao = PlatformUserDao
    if completeness <= 100:
        return 0

    redisClient = RedisClient()
    key = RedisKey.getUserCompletenessKey(user_id)
    if not redisClient.exists(key):
        originalAmount = userDao.getTokenLogByAction(user_id, AwardTokenRuleEnum.ProfileCompleteness.name)
        if originalAmount > 0:
            return 0

    amount = AwardTokenRuleEnum.ProfileCompleteness.__getattribute__("maxamount")
    userDao.updateTokenCount(user_id, AwardTokenRuleEnum.ProfileCompleteness.name, int(amount))

    redisClient.set(key, amount)
    redisClient.setExpire(key, 86400)

    awardKey = RedisKey.getDailyActionAwardTokenKey(user_id, AwardTokenRuleEnum.ProfileCompleteness.name,
                                                    datetime.today())
    redisClient.incr(awardKey, amount)
    redisClient.setExpire(awardKey, 86400)

    return amount


async def calcAwardTokenByRule(userId, action):
    userDao = PlatformUserDao
    if action == AwardTokenRuleEnum.ProfileCompleteness.name:
        return

    redis = RedisClient()
    # 幂等检查 + 日限额检查（Redis）
    key = RedisKey.getDailyActionAwardTokenKey(userId, action, datetime.today())
    todayTotal = redis.get(key)
    if todayTotal is None:
        todayTotal = 0

    canAward = min(action.amount, action.dailyLimit - todayTotal)
    if canAward > 0:
        userDao.updateTokenCount(userId, action, canAward)
        redis.incr(key, canAward)
        redis.expire(key, 86400)
        key = RedisKey.getUserTokenCountKey(userId)
        redis.delete(key)

def calcCompletenessAndToken(profile: PlatformUserProfileModel,role:str):
    userDao = PlatformUserDao
    score = 0
    if profile.display_name: score += WeightEnum.display_name.value

    if profile.bio: score += WeightEnum.bio.value

    if profile.city:  score += WeightEnum.city.value

    if profile.skill_tags:  score += WeightEnum.skill_tags.value

    if profile.industry_tags: score += WeightEnum.industry_tags.value

    if profile.avatar_url: score += WeightEnum.avatar_url.value

    if profile.skill_tags: score += WeightEnum.skill_tags.value

    if role==UserRoleEnum.FOUNDER:
        if profile.project_name:  score += WeightEnum.project_name.value
        if profile.funding_stage or profile.project_stage:  score += WeightEnum.funding_stage.value
        if profile.need_tags:  score += WeightEnum.needTags.value
    if role==UserRoleEnum.INVESTOR:
        if profile.investment_tags: score += WeightEnum.investment_stages.value

    updateProfileCompleteness(profile.user_id,score)
    tokenCount = calcTokenForRegister(profile.user_id,score)
    redis = RedisClient()
    completenessKey = RedisKey.getUserCompletenessKey(profile.user_id)
    redis.set(completenessKey, score)

    return (score,tokenCount)

