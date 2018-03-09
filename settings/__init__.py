#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/10/19 下午3:58
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : __init__.py
# @Software: PyCharm
import logging
import importlib
from importlib import import_module
from functools import partial
from toolkit.cmdline import cmdline

__author__ = 'blackmatrix'
#
#
# def import_settings():
#     config = cmdline.config
#     try:
#         # import_module('local_settings.{}'.format(config))
#         exec('from local_settings.{} import *'.format(config))
#     except ImportError:
#         # import_module('settings.{}'.format(config))
#         exec('from settings.{} import *'.format(config))
#     logging.info('config name: {}'.format(config))
#
#
# import_settings()