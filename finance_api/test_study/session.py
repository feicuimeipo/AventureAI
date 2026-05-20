# -*- coding: utf-8 -*-
import os

import flask.sessions
from flask import Flask

app = Flask(__name__)

# os.urandom(24) 生成随机数种子
# 启用session: SECRET_KEY配置好后
# 客户端会多一个sesion的cookie
app.config['SECRET_KEY'] = os.urandom(24)


@app.route("/")
def index():
    return "hello world!"


@app.route("/add_session")
def addSession():
    flask.session["username"] = "大念老师"
    flask.session["nickname"] = "zhouge"
    flask.session["role"] = "admin"
    return 'session设置成功'


@app.route("/get_session")
def getSession():
    username = flask.session.get("username")
    nickname = flask.session.get("nickname")
    role = flask.session.get("role")
    return 'username={}, nickname={}, role={}'.format(username, nickname, role);


@app.route("/del_session")
def deleteSession():
    flask.session.clear()
    # flask.session.pop("username")
    # flask.session.pop("nickname")
    # flask.session.pop("role")
    return  "delete successfully"


if __name__ == '__main__':
    app.run()
