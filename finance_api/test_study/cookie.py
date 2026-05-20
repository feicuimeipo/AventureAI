# -*- coding: utf-8 -*-
import datetime

import flask
from flask import Flask, make_response

app = Flask(__name__)


@app.route("/")
def index():
    return "设置cookie"


# 设置cookie
@app.route("/cookie")
def cookie():
    response = make_response("设置cookie")
    # max_age:单位 秒， 10秒后过期
    # response.set_cookie("name", "teacher", max_age=10)

    # 设置一天后过期
    expire_time = datetime.datetime.now() + datetime.timedelta(days=1)
    response.set_cookie("name", "大念", expires=expire_time)
    response.set_cookie("sex", "女", expires=expire_time)
    response.set_cookie("city", "北京", expires=expire_time)
    # 操作时需要将response返回到前端，否则操作不成功
    return response


# 返回cookie
@app.route("/get_cookie")
def getCookie():
    cookies = flask.request.cookies
    cookies_dict = cookies.to_dict()

    for k, v in cookies_dict.items():
        print("{} = {}".format(k, v))
    name = cookies_dict.get("name")
    return "name={}".format(name)


@app.route("/del_cookie")
def deleteCookie():
    response = make_response("删除cookies成功")
    response.delete_cookie("name")
    response.delete_cookie("sex")
    response.delete_cookie("city")

    # 操作时需要将response返回到前端，否则操作不成功
    return response


if __name__ == '__main__':
    app.run()
