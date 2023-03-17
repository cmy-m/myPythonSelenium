#! /usr/bin/env python3
# _*_ coding: utf-8 _*_
# Copyright (C) mileschen
import os


# 放在项目根目录下，用于获取项目路径
def get_current_path(arg: int = 0):
    """
    -返回执行文件所在目录(哪里调用这个函数就返回哪里的路径)，不包含文件名

    :arg: 控制目录的缩进，默认不缩进
    :return:
    """
    if arg == 0:
        return os.path.abspath(os.getcwd())
    elif arg < 0:
        raise ValueError('arg不能为负数')
    else:
        v = '..'
        for x in range(arg):
            v += os.path.sep + '..'
        return os.path.abspath(os.getcwd() + v)


def get_filepath(arg: int = 0):
    """
    -该文件放在哪里目录就返回哪个目录的路径，不包含文件名

    :arg: 控制目录的缩进，默认不缩进
    :return:
    """
    if arg == 0:
        return os.path.dirname(__file__)
    elif arg < 0:
        raise ValueError('arg不能为负数')
    else:
        v = '..'
        for x in range(arg):
            v += os.path.sep + '..'
        return os.path.abspath(os.path.dirname(__file__) + v)


def add_path(path1):
    """
    返回path1的绝对路径
    :param path1:相对路径
    :return:
    """
    return os.path.join(get_filepath(), path1)

# os.path.dirname(path)  : 返回path最后一个斜杠之前的所有内容，如果path包含文件名则去掉文件名返回，如果不包含文件名则去掉末尾级目录返回
# os.path.abspath(path)  :返回path路径的绝对路径，如果path后有/../..  每一个/..代表缩进一个目录
# os.path.sep+'.'  :控制不同平台路径分隔符
# os.path.join(a, b, c)   :将字符串abc按目录格式拼接输出，自动匹配不同平台的路径分隔符
# Windows和Linux 路径反斜杠与正斜杠解决方案：os.path.join 或者 os.path.sep 或者 path.replace('\\', '/') 或者 使用pathlib模块pathlib.path()
# os.path.relpath(path, start)  :获取start到path的相对路径
