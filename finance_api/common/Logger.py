# -*- coding: utf-8 -*-
import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler

import colorlog

from app.config import EnvConfig


def getLogger(name="myApp"):
    if name.__contains__("/"):
        ary = name.split("/")
        name = ary[len(ary)-1]
    logger = logging.getLogger("myApp")
    # 避免重复添加 handler
    if logger.handlers:
        return logger


    logger.setLevel(EnvConfig.LOG_LEVEL)
    # 创建控制台 Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # 定义日志格式，%(log_color)s 会被替换为对应级别的颜色代码
    #log_format = "%(log_color)s%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s"
    log_format = "%(log_color)s%(asctime)s - [%(levelname)s] - %(name)s:%(filename)s:%(lineno)d- %(message)s"

    # 定义不同级别对应的颜色
    color_config = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
    # 创建彩色格式化器
    formatter = colorlog.ColoredFormatter(
        fmt=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors=color_config
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


    # 日志记录器： 日志路径与文件，maxBytes日志文件的最大在大小-30M，backupCount-日志最大个数
    # when='D': 按天轮转
    # interval=1: 每1天轮转一次
    # backupCount=7: 保留最近7天的日志文件，超出的自动删除
    log_file_path = EnvConfig.LOG_FILE_PATH
    log_dir = os.path.dirname(log_file_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    file_log_handler = TimedRotatingFileHandler(
        filename="log/app.log",
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    # 设置轮转后的文件名后缀格式 (例如: app.log.2026-04-23)
    file_log_handler.suffix = "%Y-%m-%d"

    # 3. 重要：必须更新 extMatch 正则，否则删除旧日志时会找不到文件
    # 默认正则可能不匹配你自定义的日期格式，需手动编译
    file_log_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    file_log_handler.setLevel(EnvConfig.LOG_LEVEL)
    file_log_handler.setFormatter(formatter)
    logger.addHandler(file_log_handler)

    return logger
