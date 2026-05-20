import datetime

REDIS_KEY_USER_REGISTER="user_register_verificationCode:%s"
REDIS_KEY_USER_FORGET_PASSWORD="user_forget_password:%s"
REDIS_KEY_AUTH_TOKEN="Bearer:%s"
REDIS_KEY_USER_DETAIL="user_detail:%s"
REDIS_KEY_UPDATE_USER_PROFILE="update_user_profile:%s"

def getDailyActionAwardTokenKey(userId,action,datetime):
    return f"user_daily_award_token:{userId}:{action}:{datetime}"

def getUserTokenCountKey(userId):
    return f"user_daily_award_token_count:{userId}"

def getUserCompletenessKey(userId):
    return f"user_profile_completeness:{userId}"


def getUserBehavior(userId:str,timedelta_days=0):
    time = datetime.datetime.now()
    if timedelta_days<0:
        time - datetime.timedelta(days=abs(timedelta_days))
    else:
        time + datetime.timedelta(days=abs(timedelta_days))

    now = f'{time.year}-{time.month}-{time.day}'
    return f"user_behavior_{now}:behavior_{userId}"

def getUserBehavior_daily_duration_field():
    return 'duration'

def getUserBehavior_last_activity_field():
    return 'last_activity_timestamp'

def getUserBehavior_browse_count_field():
    return 'browse_count'

def getUserBehavior_message_count_field():
    return 'message_count'

def getUserBehavior_login_count_field():
    return 'login_count'

def getUserStatKey_daily_login_count(userId:str,timedelta_days=0):
    time = datetime.datetime.now()
    if timedelta_days<0:
        time - datetime.timedelta(days=abs(timedelta_days))
    else:
        time + datetime.timedelta(days=abs(timedelta_days))

    now = f'{time.year}-{time.month}-{time.day}'
    return f"user_behavior_{now}:behavior_login_count_{userId}"


def getInteractionListKey(from_user_id,to_user_id,result_id):
    return f'partner_match_intereaction_list: {result_id}_{from_user_id}_{to_user_id}'

def getMatchResultDetailKey(result_id):
    return f'partner_match_result_detail: {result_id}'


def getMatchResultScoreKey(result_id):
    return f'partner_match_result_detail_score: {result_id}'


