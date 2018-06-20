#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/3/14 下午2:07
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: urls.py
# @Software: PyCharm
from . import views
from django.urls import path
from .config import current_config

__author__ = 'blackmatrix'

from . import auto_register_webapi

urlpatterns = [
    path('<version>/<method>', views.api_routing, name='api_routing'),
]

auto_register_webapi()
