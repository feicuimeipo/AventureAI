import uuid
from datetime import datetime
from decimal import Decimal

from _schedule.celery_app import celery_app
from advance_search.ai import embedding_generator
from advance_search.ai.reason_generator import ReasonGenerator
from advance_search.vector import milvus_conn
from advance_search.vector.milvus_user_profile_manager import UserProfileVector
from app.config import EnvConfig
from common import RedisKey
from common.Logger import getLogger
from common.Redis import RedisClient
from database.common import PlatformUserManager
from database.dao import PlatformUserDao, PlatformDataSynchronizationDao, PlatformUserStatDao
from database.entity.PlatformMatchResults import PlatformMatchResultModel

logger = getLogger('--task_partner_match---')


@celery_app.task(name='partner_match_based_on_need', bind=True, max_retries=3)
def partner_match_based_on_need(self,need_id=None):
    logger.info(f"--开始{partner_match_based_on_need}---")
    userDao = PlatformUserDao
    dataSyncDao = PlatformDataSynchronizationDao
    userStatDao = PlatformUserStatDao
    userVector = UserProfileVector(milvus_conn.getMilvusClient())
    reasonGenerator = ReasonGenerator()
    dataList = []
    need_embeddings = []
    needList = dataSyncDao.get_cofounder_need(need_id)
    logger.info(f"--需求个数: {len(needList)}---")
    for need in needList:
        embeddings_profile_text = embedding_generator.build_need_text(need)
        if EnvConfig.IS_MOCK.lower() == 'true':
            embedding  = embedding_generator.getEmbeddingMockData()
        else:
            embedding = embedding_generator.generate_user_embedding(embeddings_profile_text)

        if embedding:
            need.embedding = embedding

            roleWanted = need.role_wanted
            city_reqs = need.city_reqs if need.city_reqs else []
            city_reqs.append("All_RemoteCapability")

            roles = []
            if roleWanted.lower() in ['newproject']:
                roles.append(PlatformUserManager.UserRoleEnum.FOUNDER.value)
            elif roleWanted.lower() in ['investor','resource','resourceprovider']:
                roles.append(PlatformUserManager.UserRoleEnum.INVESTOR.value)
                roles.append(PlatformUserManager.UserRoleEnum.GOV.value)
                roles.append(PlatformUserManager.UserRoleEnum.CORP.value)
            else:
                roles.append(PlatformUserManager.UserRoleEnum.FOUNDER.value)
                roles.append(PlatformUserManager.UserRoleEnum.INVESTOR.value)
                roles.append(PlatformUserManager.UserRoleEnum.GOV.value)
                roles.append(PlatformUserManager.UserRoleEnum.CORP.value)

            filter_expr = {
                "role not in ["+ ",".join(roles) +"] and city in ["+ ",".join(city_reqs) +"]"
            }

            results = userVector.search_vectors(need.embedding, 200, filter_expr)

            userIds = []
            userIds.extend(item["user_id"] for item in results)
            userStatList = userStatDao.getUserStats(userIds)
            for result in results:
                try:
                    seekers = dataSyncDao.get_user_profile(need.user_id, "partner_match")
                    candidate = userDao.getProfileById(result["user_id"])
                    if len(seekers) == 0 or not candidate: continue;

                    semantic_score = convert_milvus_distance_to_score(result["distance"])
                    role_score = calculate_role_complementarity(candidate.title,roleWanted)
                    skill_score = calculate_skill_matching(candidate.skill_tags , need.skill_reqs)
                    active_score = calculate_activity_coefficient(userStatList, str(candidate.user_id))
                    geo_score = calculate_location_match(candidate.city, city_reqs)
                    industry_score = calculate_industry_jaccard_similarity(
                        candidate.industry_tags,candidate.skill_tags,[need.industry], need.skill_reqs
                    )

                    score_total = (semantic_score * 100 * 0.35 + skill_score * 0.25 +
                             role_score * 0.20 + active_score * 0.12 + geo_score * 0.08)

                    funding_stage = 0
                    if seekers[0].role in ['investor', 'gov', 'corp']:
                        funding_stage = calculate_stage_match_score(candidate.funding_stage, seekers[0].investment_tags)

                    reasons = None
                    if EnvConfig.IS_MOCK.lower() != "true":
                        reasons = ["有战略眼光", "技术牛人", "在创业充满热情"]
                    else:
                        reasons = reasonGenerator.gen_reasons(need.description, need.skill_tags, candidate.bio,
                                                              candidate.skill_tags)

                    matchResult = PlatformMatchResultModel()
                    matchResult.seeker_id = need.user_id
                    matchResult.candidate_id = candidate.user_id
                    matchResult.need_id = need.id
                    matchResult.score_total = Decimal.from_float(score_total)
                    matchResult.score_detail = {
                        "total": round(score_total, 1),
                        "semantic": round(semantic_score * 100, 1),
                        "skill": round(skill_score, 1),
                        "role": round(role_score,1),
                        "active": active_score,
                        "geo": round(geo_score,1),
                        "industry":round(industry_score,1),
                        "funding_stage": round(funding_stage,1)
                    }
                    matchResult.reasons = reasons if reasons else []
                    matchResult.computed_at = datetime.now()
                    matchResult.match_resource = "cofounder_need"
                    matchResult.is_featured = False

                    matchResult.id = uuid.uuid4()
                    dataList.append(matchResult)

                except Exception as e:
                    logger.error(f'str{e}')
                need_embeddings.append(need)

            try:
                if len(dataList) > 0:
                    dataSyncDao.insert_match_results(dataList, "cofounder_need")
                    dataSyncDao.update_cofounder_embedding_status(need_embeddings)
            except Exception as e:
                logger.error(f'str{e}', exc_info=True)
    logger.info(f'--partner_match_based_on_need--结束--')

@celery_app.task(name='partner_match_based_on_user_profile', bind=True, max_retries=3)
def partner_match_based_on_user_profile(self,uid=None):
    logger.info(f'--partner_match_based_on_user_profile--开始--')
    userDao = PlatformUserDao
    dataSyncDao = PlatformDataSynchronizationDao
    userStatDao = PlatformUserStatDao
    userVector = UserProfileVector(milvus_conn.getMilvusClient())
    matchResultList = []
    userProfiles = dataSyncDao.get_user_profile(uid,'partner_match')

    reasonGenerator = ReasonGenerator()
    for user in userProfiles:
        seek_id = user.user_id
        embedding = user.embedding
        if len(embedding)>0:
            cities = [user.city,"All_RemoteCapability"]
            filter_expr = {f"city in [{ ",".join(cities) }]"}
            results = userVector.search_vectors(embedding, 200, filter_expr)

            userIds = []
            userIds.extend(item["user_id"] for item in results)
            userStatList = userStatDao.getUserStats(userIds)
            for result in results:
                try:
                    candidate_id = result["user_id"]
                    milvus_distance = result["distance"]
                    candidate = userDao.getProfileById(candidate_id)
                    semantic_score = convert_milvus_distance_to_score(milvus_distance)
                    role_score = calculate_role_complementarity(candidate.title, user.title)
                    skill_score = calculate_skill_matching(candidate.skill_tags, user.skill_tags)
                    active_score = calculate_activity_coefficient(userStatList, candidate_id)
                    geo_score = calculate_location_match(candidate.city, [user.city])

                    score_total = (semantic_score * 100 * 0.35 + skill_score * 0.25 +
                                   role_score * 0.20 + active_score * 0.12 + geo_score * 0.08)
                    industry_score = calculate_industry_jaccard_similarity(
                        candidate.industry_tags,candidate.skill_tags,user.industry_tags, user.skill_tags
                    )

                    reasons = None
                    if EnvConfig.IS_MOCK.lower() == "true":
                        reasons = ["有战略眼光", "技术牛人", "在创业充满热情"]
                    else:
                        reasons = reasonGenerator.gen_reasons(user.bio,user.skill_tags,candidate.bio, candidate.skill_tags)

                    matchResult = PlatformMatchResultModel()
                    matchResult.seeker_id = user.user_id
                    matchResult.candidate_id = candidate.user_id
                    matchResult.need_id = "00000000-0000-0000-0000-000000000000"
                    matchResult.score_total = Decimal.from_float(score_total)


                    funding_stage = 0
                    if user.role in ['investor', 'gov', 'corp']:
                        funding_stage = calculate_stage_match_score(candidate.funding_stage, user.investment_tags)

                    matchResult.score_detail = {
                        "total": round(score_total, 1),
                        "semantic": round(semantic_score * 100, 1),
                        "skill": round(skill_score * 100, 1),
                        "role": round(role_score * 100, 1),
                        "active": active_score * 100,
                        "geo": round(geo_score * 100, 1),
                        "industry": round(industry_score * 100, 1),
                        "funding_stage": round(funding_stage * 100, 1)
                    }
                    matchResult.reasons = reasons if reasons else None
                    matchResult.computed_at = datetime.now()
                    matchResult.match_resource = "user_profile"
                    matchResult.id = uuid.uuid4()
                    matchResult.is_featured = False
                    matchResult.algo_version = ''
                    matchResultList.append(matchResult)
                except Exception as e:
                    logger.error(f'str{e}')
            try:
                if len(matchResultList)>0:
                    dataSyncDao.insert_match_results(matchResultList, "user_profile")
                    dataSyncDao.update_user_profile_match_datetime(userProfiles)
            except Exception as e:
                logger.error(f'str{e}')
    logger.info(f'--partner_match_based_on_user_profile--结束--')


# 1. 语义相似度
def convert_milvus_distance_to_score(distance: float, metric_type: str = "COSINE") -> float:
    """
    将 Milvus 返回的 distance 转换为 0-100 的相似度分数

    :param distance: Milvus 搜索返回的 distance 值
    :param metric_type: 创建 Collection 时使用的度量类型 ("COSINE", "L2", "IP")
    :return: 0-100 的相似度分数
    """
    if metric_type == "COSINE":
        # COSINE 模式下，distance = 1 - cosine_similarity
        # cosine_similarity = 1 - distance
        # 分数 = cosine_similarity * 100
        score = (1 - distance) * 100

    elif metric_type == "L2":
        # L2 模式下，distance 越小越相似，无固定上限
        # 使用 sigmoid 或倒数归一化到 0-100 仅为示例，具体需根据数据分布调整
        # 这里使用 1 / (1 + distance) 进行简单归一化
        similarity = 1 / (1 + distance)
        score = similarity * 100

    elif metric_type == "IP":
        # IP (Inner Product) 模式下，通常值越大越相似
        # 如果 Milvus 返回的是原始 IP 值，则直接映射
        # 注意：IP 值范围取决于向量归一化情况，若向量已归一化，IP 等价于 Cosine
        # 假设向量已归一化，IP 范围 [-1, 1] 或 [0, 1]，需根据实际情况调整
        # 此处假设等价于 Cosine 处理，若未归一化则不能直接这样转
        score = (1 - distance) * 100  # 仅当 IP 被当作距离处理时，通常 IP 不转为 distance

    else:
        raise ValueError(f"Unsupported metric type: {metric_type}")

    return round(score, 2)


#### 维度2：技能匹配度（用 SQL）
def calculate_skill_matching(
        cofounder_skill_ids: list[str],  # ['skill_1', 'skill_2', ...]
        required_skill_ids: list[str]  # ['skill_1', 'skill_3', ...]
) -> float:
    """
    计算 Jaccard 相似度
    """

    set1 = set(cofounder_skill_ids)
    set2 = set(required_skill_ids)

    if len(set2) == 0:
        # 如果需求没有指定必需技能，则评分最高
        return 100.0

    intersection = len(set1 & set2)  # 交集
    union = len(set1 | set2)  # 并集

    if union == 0:
        return 0.0

    jaccard_similarity = intersection / union

    # 转换成 0-100
    score = jaccard_similarity * 100

    return score

#### 维度3：角色互补性（用规则表）
Role_Complementarity_Matrix = {
    ('CEO', 'CTO'): 95,
    ('CEO', 'CMO'): 92,
    ('CEO', 'CFO'): 90,
    ('CEO', 'COO'): 88,
    ('CTO', 'CMO'): 85,
    ('CTO', 'CFO'): 80,
    ('CTO', 'COO'): 82,
    ('CMO', 'CFO'): 75,
    ('CMO', 'COO'): 80,
    ('CFO', 'COO'): 78,
    # --- 相同角色互补度最低 ----
    ('CTO', 'CTO'): 20,
    ('CMO', 'CMO'): 20,
    ('CEO', 'CEO'): 30,  # CEO可以有多个联合创始人
}


def calculate_role_complementarity(
        candidate_role: str,
        required_role: str
) -> float:
    """
    查表返回角色互补度
    """

    # 尝试查询 (cofounder_role, required_role)
    key = (candidate_role, required_role)

    if key in Role_Complementarity_Matrix:
        return float(Role_Complementarity_Matrix[key])

    # 尝试反向查询 (required_role, cofounder_role)
    reverse_key = (required_role, candidate_role)
    if reverse_key in Role_Complementarity_Matrix:
        return float(Role_Complementarity_Matrix[reverse_key])

    # 如果没找到，返回中等分数
    return 50.0



#### 维度4：活跃度系数（用 Redis）
def calculate_activity_coefficient(userStatList, user_id: str) -> float:
    """
    计算用户过去7天的活跃度
    """
    redis_client = RedisClient()

    # 从 Redis 获取行为数据
    userBehaviorKey = RedisKey.getUserBehavior(user_id,0)
    lastActiveTimeField = RedisKey.getUserBehavior_last_activity_field()
    browseCountField = RedisKey.getUserBehavior_browse_count_field()
    messageCountField = RedisKey.getUserBehavior_message_count_field()
    #dailyDurationField = RedisKey.getUserBehavior_daily_duration_field()
    loginCountKey = RedisKey.getUserStatKey_daily_login_count(user_id)

    lastActiveTime = redis_client.hget(userBehaviorKey,lastActiveTimeField)
    browseCount = redis_client.hget(userBehaviorKey, browseCountField)
    messageCount = redis_client.hget(userBehaviorKey, messageCountField)
    loginCount = redis_client.get(loginCountKey)

    if not lastActiveTime:
        for stat in userStatList:
            if user_id == str(stat.user_id):
                lastActiveTime = stat.last_active_time
                browseCount = stat.browse_count
                messageCount = stat.message_count
                loginCount = stat.login_count_7days

    if not lastActiveTime and not browseCount or not messageCount or not loginCount:
        # 该用户没有活动记录
        return 20.0

    login_count = int(loginCount)
    browse_count = int(browseCount)
    message_count = int(messageCount)
    last_active_ts = int(lastActiveTime)

    # 计算活跃度
    # 登录频率最重要（每次登录5分），浏览其次（每次1分），消息最后（每条2分）
    activity_score = (
            login_count * 5 +
            browse_count * 1 +
            message_count * 2
    )

    # 考虑最后活跃时间（指数衰减）
    # 7天以内很活跃，超过7天活跃度衰减
    now = datetime.now().timestamp()
    days_since_active = (now - last_active_ts) / (24 * 3600)

    if days_since_active <= 1:
        time_decay = 1.0
    elif days_since_active <= 3:
        time_decay = 0.8
    elif days_since_active <= 7:
        time_decay = 0.6
    elif days_since_active <= 14:
        time_decay = 0.4
    else:
        time_decay = 0.2

    final_activity_score = min(activity_score * time_decay, 100)

    return float(final_activity_score)


#### 维度5：地理位置匹配（用 SQL）
def calculate_location_match(
        candidate_city: str,
        need_cities: list[str]
) -> float:
    """
    计算创业者所在城市与需求城市的匹配度

    target_cities 例如：['北京', '可远程']
    cofounder_city 例如：'北京'
    """

    if not need_cities:
        # 如果需求没有限定城市，则得分最高
        return 100.0

    # 检查是否精确匹配
    if candidate_city in need_cities:
        return 100.0

    # 检查是否支持远程
    if '可远程' in need_cities or 'remote' in need_cities:
        return 80.0

    # 检查是否在同一地区（可选）
    # 比如如果需求在"北京周边"，"燕郊"也可以接受
    NEARBY_CITIES = {
        '北京': ['燕郊', '固安', '昌平'],
        '上海': ['昆山', '嘉兴', '松江'],
        '深圳': ['东莞', '惠州', '广州'],
    }

    if candidate_city in NEARBY_CITIES.get(need_cities[0], []):
        return 60.0

    # 都不匹配
    return 20.0

def calculate_industry_jaccard_similarity(candidate_industries,candidate_skills,need_industries,need_skills) -> float:
    """
    计算两个标签集合的 Jaccard 相似度
    :param person_a_tags: list, 人员A的行业/技能标签列表
    :param person_b_tags: list, 人员B的行业/技能标签列表
    :return: float, 相似度 (0-1)
    """
    candidate_industries.extend(candidate_skills)
    need_industries.extend(need_skills)
    set_a = set(candidate_industries)
    set_b = set(need_industries)

    # 如果两者都为空，定义相似度为 0 或 1 (视业务逻辑而定，这里设为0)
    if not set_a and not set_b:
        return 0.0

    # 计算交集和并集
    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)

    if not union:
        return 0.0

    jaccard_score = len(intersection) / len(union)
    return round(jaccard_score, 4)

    # 示例数据
    # person_a = ["Python", "AI", "金融", "数据分析", "SQL"]
    # person_b = ["Python", "Java", "金融", "后端开发", "SQL"]
    #
    # score = calculate_jaccard_similarity(person_a, person_b)
    # print(f"Jaccard 行业背景匹配度: {score}")


def calculate_stage_match_score(startup_stage, investor_stages):
    """
    计算阶段匹配得分
    如果创业阶段在投资人偏好列表中，得满分；否则根据邻近程度扣分
    """
    stage_order = ["Seed", "Angel", "PreA", "A", "B_B+"]

    if startup_stage not in stage_order:
        return 0.0

    if startup_stage in investor_stages:
        return 1.0

    # 如果不在偏好列表中，计算距离惩罚
    startup_idx = stage_order.index(startup_stage)
    min_distance = float('inf')
    for inv_stage in investor_stages:
        if inv_stage in stage_order:
            inv_idx = stage_order.index(inv_stage)
            distance = abs(startup_idx - inv_idx)
            min_distance = min(min_distance, distance)

    # 每偏离一个阶段，得分降低 0.3
    score = max(0, 1.0 - (min_distance * 0.3))
    return score


# app = Flask(__name__)
# _schedule = make_celery(app)
# partner_match_based_on_need('c8af8723-0088-43e0-b6b2-7e9b2451eddb')
# _schedule.send_task("partner_match.partner_match_based_on_user_profile", args=['5d4d6c34-ced1-4c18-b9c6-b25ec1135ee4'])

