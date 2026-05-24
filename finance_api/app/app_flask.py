import os

from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

import settings
from app.config import EnvConfig
from common.Logger import getLogger


def init_scheduler():
    pass
    # scheduler = BackgroundScheduler()
    # # 添加任务...
    # scheduler.start()


def init_swagger_ui(app):
    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/static/openapi.json'  # Our API url (can of course be a local resource)
    # Call factory function to create our blueprint
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "petstore",
        },
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )
    app.register_blueprint(swagger_ui_blueprint,url_prefix=SWAGGER_URL)


# 注册蓝图
def init_blueprint(app):
    from controller.TemplateController import template
    from controller.CurrentUserController import currentUser
    from controller.UserLoginController import userLogin
    from controller.UserRegisterController import userRegister
    from controller.UserForgetPasswordController import forgetPassword
    from controller.NeedsController import needBt
    from controller.PartnerMatchController import partnerMatchBP

    # 注册蓝图
    app.register_blueprint(currentUser)
    app.register_blueprint(template)
    app.register_blueprint(userLogin)
    app.register_blueprint(userRegister)
    app.register_blueprint(forgetPassword)
    app.register_blueprint(needBt)
    app.register_blueprint(partnerMatchBP)


def create_flask_app():
    # 配置模板，静态资源及静态的上下文路径
    app = Flask(__name__, template_folder="../template", static_url_path="/", static_folder="../static")

    # 启用session
    # os.urandom - 生成随机种子，用于生成: session_id
    app.config['SECRET_KEY'] = os.urandom(24)

    # 配置Flask和Celery
    app.config.update(
        CELERY_BROKER_URL=EnvConfig.CELERY_BROKER_URL,
        CELERY_RESULT_BACKEND=EnvConfig.CELERY_BROKER_URL
    )

    getLogger(__name__)
    init_blueprint(app)
    init_swagger_ui(app)
    init_scheduler()

    #默认允许所有域名
    if settings.cros:
        CORS(app,
             resources={r"/*": {"origins": ["http://localhost","http://127.0.0.1","http://www.915zb.com", "http://915zb.com","http://api.915zb.com","https://www.015zb.com", "https://915zb.com","https://api.915zb.com"]}},
             supports_credentials=True,
             origins=["http://localhost","http://127.0.0.1","http://www.915zb.com", "http://915zb.com","http://api.915zb.com","https://www.015zb.com", "https://915zb.com","https://api.915zb.com"],
             methods=["GET", "POST", "PUT", "DELETE"],
             allow_headers=["Content-Type", "X-Token", "Authorization"],
             expose_headers=["X-Total-Count", "X-Page-Number"])

    return app
