# -*- coding: utf-8 -*-

from flask import Flask, request

from common.Logger import getLogger

app = Flask(__name__)

logger = getLogger()

@app.route("/post1", methods=["POST"])
def post1():
    return "这是我的第一个post请求"


# form格式的参数
@app.route("/post2", methods=["POST"])
def post2():
    username = request.form["username"]
    password = request.form["password"]
    logger.info("username=" + username)
    logger.info("password=" + password)
    return "{},您好".format(username)


# form格式的参数
@app.route("/post3", methods=["POST"])
def post3():
    request_data = request.get_json();
    logger.info("requestData:{},类型为{}".format(request_data, type(request_data)))
    # 得到具体的值
    username = request_data["username"]
    password = request_data["password"]
    logger.info("username=" + username)
    logger.info("password=" + password)
    return "{},您好".format(username)

if __name__ == '__main__':
    app.run()
