#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/4 上午11:03
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : manager.py
# @Software: PyCharm
import importlib
from tornado.ioloop import IOLoop
from tornado.concurrent import Future
from .config import default, set_apizen_config
"""
-------------------------------
ApiZen初始化管理模块
-------------------------------
适用版本：Tornado
"""

__author__ = 'blackmatrix'


class ApiZenManager:

    def __init__(self, config):
        self.config = config
        # 复制传入的配置信息
        self.copy_current_config()
        # 导入Api版本
        self.import_api_versions(versions=config.get('APIZEN_VERSIONS'))

    # 导入Api版本
    @staticmethod
    def import_api_versions(versions):
        if versions:
            for version in versions:
                importlib.import_module(version)

    # 复制当前的配置文件到ApiZen
    def copy_current_config(self):
        for k, v in default.items():
            set_apizen_config(k, self.config.get(k, default[k]))


ioloop = IOLoop.instance()


def async(task, *args, **kwargs):
    future = Future()
    result = task.delay(*args, **kwargs)
    IOLoop.instance().add_callback(_on_result, result, future)
    return future


def _on_result(result, future):
    if result.ready():
        future.set_result(result.result)
    else:
        IOLoop.instance().add_callback(_on_result, result, future)


if __name__ == '__main__':
    pass
