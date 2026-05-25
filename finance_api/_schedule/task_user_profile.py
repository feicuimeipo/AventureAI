from datetime import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _schedule import task_partner_match
from _schedule.celery_app import celery_app
from advance_search.ai import embedding_generator
from advance_search.vector import milvus_conn
from advance_search.vector import milvus_user_profile_manager
from app.config import EnvConfig
from common import RedisKey
from common.Logger import getLogger
from common.Redis import RedisClient
from database.dao import PlatformDataSynchronizationDao, PlatformUserStatDao, PlatformUserDao, PlatformCeleryTaskLogDao
from database.entity.PlatformCeleryTaskLog import PlatformCeleryTaskLogModel
from database.entity.PlatformUserProfile import PlatformUserProfileModel

logger = getLogger('--task_user_profile---')
@celery_app.task(name='transform_user_profile_into_milvus', bind=True, max_retries=3)
def transform_user_profile_into_milvus(self,user_id=None):
    logger.info("milvus同步开始!")
    dataSyncDao = PlatformDataSynchronizationDao
    vectorManger: milvus_user_profile_manager.UserProfileVector = None

    celeryTaskLogList = []
    try:
        milvusClient = milvus_conn.getMilvusClient()
        milvus_user_profile = milvus_user_profile_manager.UserProfileVector(milvusClient)
        userProfiles = dataSyncDao.get_user_profile(user_id,"transform_to_milvus")
        profiles = []
        if userProfiles and len(userProfiles) > 0:
            for userProfile in userProfiles:
                user_embedding = None
                if EnvConfig.IS_MOCK.lower() == 'true':
                    embedding_generator.getEmbeddingMockData()
                else:
                    embeddings_text = embedding_generator.build_profile_text(userProfile)
                    user_embedding = embedding_generator.generate_user_embedding(embeddings_text)

                targetProfile = PlatformUserProfileModel()
                targetProfile.user_id = userProfile.user_id
                targetProfile.embedding =user_embedding
                targetProfile.role = userProfile.role,
                targetProfile.city = userProfile.city
                profiles.append(targetProfile)

                celery_task_result = task_partner_match.partner_match_based_on_user_profile.apply_async(
                    args=[userProfile.user_id],
                    countdown=5,
                )
                celeryTaskLog = PlatformCeleryTaskLogModel()
                celeryTaskLog.task_id = celery_task_result.id
                celeryTaskLog.task_name = 'partner_match_based_on_user_profile'
                celeryTaskLog.status = celery_task_result.status
                celeryTaskLogList.append(celeryTaskLog)

            if len(profiles)>0:
                milvus_user_profile.insert_or_update(profiles)
                dataSyncDao.update_user_profile_embedding(profiles)
                PlatformCeleryTaskLogDao.batchInsertCeleryLog(celeryTaskLogList)

                logger.info("milvus同步结束-操作成功!")

    except Exception as e:
        logger.error(f"发生错误: {e}")
        raise self.retry(exc=e, countdown=60)
    finally:
        if vectorManger: vectorManger.cleanup()


@celery_app.task(name='record_user_stat',bind=True, max_retries=3)
def record_user_stat(uid=None):

    userStateDao = PlatformUserStatDao
    users = PlatformUserDao.findAllActiveUsers(uid)

    redisKeys: list[str] = []
    data_list = []
    redisClient = RedisClient()
    for u in users:
        uid = u.u.user_id
        # profile_date_at = u.p.updated_at
        try:
            userBehaviorKey = RedisKey.getUserBehavior(uid,0)
            during_field =RedisKey.getUserBehavior_daily_duration_field()
            last_activity_field = RedisKey.getUserBehavior_last_activity_field()
            browse_count_field = RedisKey.getUserBehavior_browse_count_field()
            message_count_field = RedisKey.getUserBehavior_message_count_field()

            loginCountDay_0 = RedisKey.getUserStatKey_daily_login_count(uid, 0)
            loginCountDay_1 = RedisKey.getUserStatKey_daily_login_count(uid, -1)
            loginCountDay_2 = RedisKey.getUserStatKey_daily_login_count(uid, -2)
            loginCountDay_3 = RedisKey.getUserStatKey_daily_login_count(uid, -3)
            loginCountDay_4 = RedisKey.getUserStatKey_daily_login_count(uid, -4)
            loginCountDay_5 = RedisKey.getUserStatKey_daily_login_count(uid, -5)
            loginCountDay_6 = RedisKey.getUserStatKey_daily_login_count(uid, -6)

            dailyDuration = redisClient.hget(userBehaviorKey,during_field)
            if not dailyDuration:
                dailyDuration=0
            else:
                dailyDuration = int(dailyDuration)

            lastActiveTime = redisClient.hget(userBehaviorKey,last_activity_field)
            browseCount = redisClient.hget(userBehaviorKey,browse_count_field)
            messageCount = redisClient.hget(userBehaviorKey,message_count_field)
            loginCount = (redisClient.getWithDefault(loginCountDay_0,0)
                              + redisClient.getWithDefault(loginCountDay_1,0)
                              + redisClient.getWithDefault(loginCountDay_2,0)
                              + redisClient.getWithDefault(loginCountDay_3,0)
                              + redisClient.getWithDefault(loginCountDay_4,0)
                              + redisClient.getWithDefault(loginCountDay_5,0)
                              + redisClient.getWithDefault(loginCountDay_6,0)
                              )

            dt = datetime.fromtimestamp(int(lastActiveTime)/1000) if lastActiveTime else None
            duration = min((int(dailyDuration)/1000),60) if dailyDuration else 0
            userStateModal = {
                'user_id': uid,
                'daily_duration': duration,
                'login_count_7days': loginCount,
                'last_active_time': dt,
                'browse_count': browseCount,
                'message_count': messageCount
            }

            data_list.append(userStateModal)
            redisKeys.append(userBehaviorKey)
            redisKeys.append(loginCountDay_6)
        except Exception as e:
            logger.error(e, exc_info=True)
    try:
        userStateDao.bulkInsertActivity(data_list)
        # redisClient.bulk_delete(redisKeys)
    except Exception as e:
        logger.error(e, exc_info=True)

# celery_app = Celery('task_user_profile')
# record_user_stat()
# print(datetime.fromtimestamp(1779187956408/1000))