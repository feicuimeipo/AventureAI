from gevent import monkey
monkey.patch_all()
# monkey.patch_all(ssl=False)  # 不对 ssl 进行补丁

# 导入flask
import os
from flask import request, abort
from _schedule import init_task
from _schedule.celery_app import make_celery
from app import settings
from app.app_flask import create_flask_app
from app.config import EnvConfig
from app.security import isUrlInWhite
from common import AuthToken
from common.Logger import getLogger

# 具体的代码如下：


# 配置模板，静态资源及静态的上下文路径
app = create_flask_app()
celery = make_celery(app)
init_task.startInit()
logger = getLogger((os.path.basename(__file__)))

@app.route("/")
def home():
    # raise Exception
    return "You are welcome!"

# 错误处理
@app.errorhandler(404)
def pageNotFound(e):
    logger.error(e,exc_info=True)
    abort(404,f"找不到页面{str(e)}！")

# 错误处理
# raise Exception - python抛出异常
@app.errorhandler(500)
def error(e):
    logger.error(e,exc_info=True)
    abort(500,f"服务端出错了{str(e)}！")


@app.errorhandler(Exception)
def error(e):
    logger.error(e,exc_info=True)
    abort(501,f"服务端出错了：{str(e)}！")


# 全局拉截器
@app.before_request
def beforeRequest():
    if request.path.startswith('/docs') and settings.env=='prod':
        return 'Unauthorized', 401

    # 获取请求的url，根据url判断哪些url拦截，哪些不拉截
    url = request.path
    if isUrlInWhite(url):
        pass
    else:
        """
        手动触发JWT验证流程，并将结果存入g对象
        """
        uid = AuthToken.verifyAccessToken(request)
        if uid:
            pass
        else:
            abort(401, description=f'Token验证失败')  # 如果验证失败，返回 401 状态码



# 全局上下文
@app.context_processor
def setContext():
    ctx = {
        "title": "VentureAI",
    }
    return dict(ctx=ctx)

if __name__ == '__main__':
    # flask启动
    print(EnvConfig.LOG_LEVEL)
    logger.info("开始启动....")
    app.run(host="0.0.0.0",port=EnvConfig.app_port)
    # 2.初始化服务器
    # WSGIServer(("127.0.0.1", 5000), app).serve_forever()

