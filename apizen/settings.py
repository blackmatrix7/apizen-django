#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/3/14 下午1:58
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: settings
# @Software: PyCharm
from django.conf import settings

"""
-------------------------------
ApiZen默认参数配置
-------------------------------
适用版本：Django
"""

__author__ = 'blackmatrix'

# 默认接口地址
APIZEN_ROUTE = getattr(settings, 'APIZEN_ROUTE', '/api/router/rest')

# 默认Date格式
APIZEN_DATE_FMT = getattr(settings, 'APIZEN_DATE_FMT', '%Y-%m-%d')

# 默认DateTime格式
APIZEN_DATETIME_FMT = getattr(settings, 'APIZEN_DATETIME_FMT', '%Y-%m-%d %H:%M:%S')

