# -*- coding: utf-8 -*-
from sqlalchemy import Table, create_engine, or_
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

from common.Logger import getLogger

DB_URL = 'mysql+pymysql://root:123654@47.99.219.51:3306/python_study'
Base = declarative_base()
engine = create_engine(DB_URL, echo=True)
# 打开数据库的连接会话
session = sessionmaker(engine)
# 用scoped_session - 保证线程安全
db_session = scoped_session(session)

logger = getLogger()
class TestUser(Base):
    # 表结构的反射加载 - 自动从数据库加载字段
    __table__ = Table("platform_user", Base.metadata, autoload_with=engine)


class TestComment(Base):
    # 表结构的反射加载 - 自动从数据库加载字段
    __table__ = Table("comment", Base.metadata, autoload_with=engine)


class TestFavorite(Base):
    __table__ = Table("platform_favorite", Base.metadata, autoload_with=engine)


def TestQuery():
    # filter方法，比较写的不是我们之前那种参数，它支持==<>= <= 这些运算符号
    # result = db_session.query(TestUser).filter(TestUser.username=='admin').first()

    # 之前给参数赋值的运算符是=
    result = db_session.query(TestUser).filter_by(username='admin111').first()

    logger.info(result)


def my_article():
    username = "admin"
    comments = db_session.query(TestUser, TestComment) \
        .join(TestComment, TestUser.user_id == TestComment.user_id) \
        .filter(TestUser.username == username).all()

    for user, comment in comments:
        logger.info("用户：{}, 评论：{}".format(user.username, comment.comment))


# 只返回指定的字段，-- 封装在元组里，元组外面是list
def my_article1():
    username = "admin"
    comments = db_session.query(TestUser, TestUser.username, TestComment.content) \
        .join(TestComment, TestUser.user_id == TestComment.user_id) \
        .filter(TestUser.username == username).all()

    # u - 用户名, c - content
    for user, u, c in comments:
        logger.info(user.username)
        logger.info("用户：{}, 评论：{}".format(u, c))


def my_favorite():
    username = "admin"
    list = db_session.query(TestUser, TestComment) \
        .outerjoin(TestComment, TestUser.user_id == TestComment.user_id) \
        .outerjoin(TestFavorite, TestComment.id == TestFavorite.founder_id) \
        .filter(TestUser.username == username).all()

    # u - 用户名, c - content
    for u, t in list:
        logger.info("用户：{}, 评论：{}".format(u, t))


def my_favorite1():
    keyword = "my"
    list = db_session.query(TestComment).filter(
        or_(TestComment.content.like("%" + keyword + "%"), TestComment.user_id.like("%" + keyword + "%")))

    # u - 用户名, c - content
    for u in list:
        logger.info("{}, ".format(u))


if __name__ == '__main__':
    my_favorite()
