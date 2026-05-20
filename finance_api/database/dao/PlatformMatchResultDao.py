from sqlalchemy import func, desc, Select, or_
from sqlalchemy.orm import aliased

from database.db_conn import readonly_db_session
from database.entity.PlatformCofounderNeed import PlatformCofounderNeedModel
from database.entity.PlatformMatchResults import PlatformMatchResultModel
from database.entity.PlatformUser import PlatformUserModel
from database.entity.PlatformUserProfile import PlatformUserProfileModel
from database.entity.PlatformUserStat import PlatformUserStatModel


def getCandidateDetail(id):
    SearchMatch = aliased(PlatformMatchResultModel, name="s")
    UserProfile = aliased(PlatformUserProfileModel, name="p")
    CofounderNeed = aliased(PlatformCofounderNeedModel, name="c")
    UserStats = aliased(PlatformUserStatModel, name="t")
    UserBase = aliased(PlatformUserModel, name="u")

    with (readonly_db_session() as session):
        query = (session.query(UserProfile, SearchMatch, CofounderNeed, UserStats,UserBase)
            .join(UserProfile, UserProfile.user_id == SearchMatch.candidate_id)
            .join(CofounderNeed, CofounderNeed.id == SearchMatch.need_id)
            .join(UserBase, UserBase.user_id == SearchMatch.candidate_id)
            .outerjoin(UserStats, UserStats.user_id == SearchMatch.candidate_id)
            .filter(SearchMatch.id == id))

        row = query.first()

        # -- params --
        result = row

        return result


def getCandidateMatchScoreDetail(id):
    with (readonly_db_session() as session):
        SearchMatchResult = aliased(PlatformMatchResultModel, name="s")
        stmt = Select(SearchMatchResult.score_detail).where(SearchMatchResult.id == id)
        row = session.execute(stmt)
        scoreDetail = row.score_detail
        return scoreDetail



def findMatchResult(needId, params,page:int,per_page:int):
    SearchMatchModal = aliased(PlatformMatchResultModel,name="s")
    UserBase = aliased(PlatformUserModel, name="u")
    UserProfileModal = aliased(PlatformUserProfileModel, name="p")
    offset = (page - 1) * per_page

    with readonly_db_session() as session:
        query = session.query(SearchMatchModal,
                              UserProfileModal,
                              UserBase) \
                .join(UserBase, UserBase.user_id == SearchMatchModal.candidate_id) \
                .join(UserProfileModal, UserProfileModal.user_id == SearchMatchModal.candidate_id) \
                .filter(UserBase.status == 'active')

        if params["myCandidateType"]:
            myCandidateType = params["myCandidateType"]
            if myCandidateType == 'cofounder':
                query = query.filter(UserBase.role.in_(['expert', 'fa']))
            elif myCandidateType== 'investor':
                query = query.filter(UserBase.role.in_(['investor', 'founder']))
            elif myCandidateType == 'resource':
                query = query.filter(UserBase.role.in_(['corp', 'gov']))
        elif needId:
            query = query.filter(SearchMatchModal.need_id == needId)


        query = query.distinct(SearchMatchModal.candidate_id)

        orderBy = params["orderBy"]
        if orderBy == "lastActive":
            query = query.order_by(SearchMatchModal.candidate_id, desc(UserBase.last_active))
        elif orderBy == "registerTime":
            query = query.order_by(SearchMatchModal.candidate_id, desc(UserBase.created_at))
        else:
            query = query.order_by(SearchMatchModal.candidate_id, desc(SearchMatchModal.score_total))

        rows_total = session.query(func.count()).select_from(query).scalar()
        rows = query.offset(offset).limit(per_page).all()
        # rows_total = query_total.scalar()

        # -- params --
        results = rows
        total = rows_total

        return results,total


