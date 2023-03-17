#! /usr/bin/env python3
# _*_ coding: utf-8 _*_
# Copyright (C) mileschen

from loguru import logger
import get_path


def get_logguru():
    """level = 'ERROR',
    format = '',
    filter = '',
    colorize = '',
    serialize = '',
    backtrace = '',
    diagnose = '',
    enqueue = True,    进行异步记录日志，避免丢失,用不异步操作记录日志
    catch = '',
    compression = 'zip'   设置日志文件压缩格式
    retention = '10 days'    设置日志文件保持时间
    rotation = '1 days'   设置日志文件新建周期




    @logger.catch   可以记录traceback信息
    """
    # logger.remove()
    # logger.add(sink='', format='')
    # logger.add()
    return logger

"""
需要日志的地方添加：logger.debug("日志信息")
在最终运行程序前先执行：logger.add(sink='/Users/cw/Desktop/miles/demo/log/XXXX11111.log', level='ERROR'))
"""
