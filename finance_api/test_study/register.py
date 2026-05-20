# -*- coding: utf-8 -*-

import requests
from flask import Flask, request

from common.utilities.EmailUtils import send_code

app = Flask(__name__)

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})


# 获取验证码
@app.route("/get_code")
def get_code(email):
    code = send_code(email)
    if code > 0:
        session.put("code", code)
        return 0
    else:
        return -1


# 用户注册
@app.route("/register")
def user_register():
    user_code = request.args.get("user_code")
    if user_code == session.get("code"):
        user_name = request.args.get("user_name")
        password = request.args.get("password")
        nickname = request.args.get("nickname")

        session.put("user_name",user_name)
        session.put("password", password)
        session.put("nickname", nickname)
        return '用户注册成功'
    else:
        return '注册失败,验证码错误'


# 用户登录
@app.route("/user_login")
def user_login():
    user_name = request.args.get("user_name")
    password = request.args.get("password")
    if user_name == session.get("user_name"):
        if password == session.get("password"):
            return "登录成功"
    return "用户或密码错误！"


if __name__ == "__main__":
    app.run()
