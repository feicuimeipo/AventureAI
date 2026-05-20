# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session

template = Blueprint("template", __name__, url_prefix="/api/template")

@template.route("/")
def template2():
    # session不用传递，直接在index2.html用
    session["username"] = "大念老师"
    article = {
        "title": "论Python语文的学习难度",
        "count": 200,
        "content": "我是文章<strong style='color:red'>正文</strong>"
    }
    return render_template("index.html", article=article)


# 含有公共页面 - 模板继承
@template.route("/home")
def template3():
    return render_template("home.html")


# 含有公共页面 - 模板继承
@template.route("/articleInfo")
def template4():
    return render_template("article-info.html")


# 自定义过滤器
@template.app_template_filter('/increment')
def increment(i):
    return i + 1


# 对应路由下的上下文处理（返回变量）
@template.context_processor
def templateContext():
    # 上下文处理器的返回值必须是字曲类型
    templateCtx = {
        "title": "jinja2参数传递,for循环，if判断",
        "count": 2001
    }
    return dict(templateCtx=templateCtx)


# 对应路由下的上下文处理,传入参数，返回一个函数（计算）
@template.context_processor
def templateContext1():
    # 上下文处理器的返回值必须是字曲类型
    def innerFunc(a, b):
        return a + b

    return dict(templateCtxFunc=innerFunc)
