# -*- coding: utf-8 -*-
# from asyncore import loop
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session

from app.config import EnvConfig


def db_url():
    return EnvConfig.db_url


"""
连接建立速度：
    asyncpg：毫秒级连接建立
    aiomysql：秒级连接建立
    并发处理能力：
    
    asyncpg支持更高的并发连接数
    aiomysql在中等并发下表现稳定

选择建议
    选择asyncpg的情况：    
        使用PostgreSQL数据库
        需要极致性能
        高并发场景
        选择aiomysql的情况：
    使用MySQL数据库
        项目已基于PyMySQL
        中等并发需求
最佳实践
    合理配置连接池参数：根据实际并发量调整pool_size和max_overflow
    启用连接预检查：设置pool_pre_ping=True避免连接失效
    监控连接池状态：定期检查连接池使用情况
"""


# 同步与异常代码实现指南 - https://developer.aliyun.com/article/1611594


def db_session():
    engine = create_engine(db_url(),
                           echo=EnvConfig.db_conn_if_echo,
                           pool_size=20,
                           max_overflow=10,
                           pool_pre_ping=True,
                           pool_recycle=3600,
                           # connect_args={"sslmode": "require"}
                           )

    # 打开数据库的连接会话
    session = sessionmaker(bind=engine,expire_on_commit=False)



    # 用scoped_session - 保证线程安全
    safe_session = scoped_session(session)


    return safe_session



def db_async_connect():
    async_engine = create_async_engine(
        db_url(),
        echo=EnvConfig.db_conn_if_echo,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=1500
    )
    # 打开数据库的连接会话
    session = sessionmaker(bind=async_engine, class_=AsyncSession,expire_on_commit=False)
    # 用scoped_session - 保证线程安全
    safe_session = scoped_session(session)

    return safe_session

ScopedSession = db_session()

@contextmanager
def auto_db_session():
    """
    提供自动管理的数据库会话。
    用法:
    with auto_db_session() as session:
        session.query(...)
    """
    session = ScopedSession()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        # 关键：scoped_session 必须调用 remove() 来归还连接并清理线程局部变量
        ScopedSession.close()
        ScopedSession.remove()


@contextmanager
def readonly_db_session():
    """
    语义上强调只读，实际底层仍由 ScopedSession 管理。
    主要目的是提醒开发者不要在此块中进行 write 操作。
    """
    session = ScopedSession()
    try:
        yield session
        # 只读场景通常不需要 commit，但为了保持接口一致性和清理资源，
        # 我们依然调用 remove。有些团队选择在这里显式 rollback 以确保无副作用。
        #session.rollback()
    finally:
        ScopedSession.close()
        ScopedSession.remove()