#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/3/14 下午2:07
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: urls.py
# @Software: PyCharm
from . import views
from . import settings
from django.conf.urls import url

__author__ = 'blackmatrix'

urlpatterns = [
    url('^{}/$'.format(settings.APIZEN_ROUTE), views.api_routing, name='api_routing'),
]

