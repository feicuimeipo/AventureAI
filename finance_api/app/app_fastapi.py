# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from common.Logger import getLogger
# 配置模板引擎（注意：directory 必须是字符串路径）
jinja2_templates = Jinja2Templates(directory="../template")
logger = getLogger()
# 注册蓝图
def init_router(app):
    pass

def apscheduler_job():
    pass



def create_schedule():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(apscheduler_job, 'interval', seconds=60)
    scheduler.start()

"""
用lifespan代替on_event
"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("启动前执行")
    create_schedule()
    yield
    logger.info("关闭后前执行")


def create_fastapi_app():
    # 配置模板，静态资源及静态的上下文路径
    app = FastAPI(title="AI Part",lifespan=lifespan)

    # 挂载静态文件目录（URL 路径为 /static，本地目录为 static）
    app.mount("/static", StaticFiles(directory="../static"), name="static")


    getLogger(__name__)
    init_router(app)

    return app
