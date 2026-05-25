import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _schedule.celery_app import celery_app
from common.Logger import getLogger

logger = getLogger("__init_task__")
def startInit():
    try:
        celery_app.send_task('partner_match_based_on_need')
        celery_app.send_task('transform_user_profile_into_milvus')
    except Exception as e:
        logger.error(f'{str(e)}')