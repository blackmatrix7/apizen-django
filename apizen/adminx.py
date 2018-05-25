#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/5/25 下午4:05
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: adminx
# @Software: PyCharm
import xadmin
from.models import ApiZenRequest


@xadmin.sites.register(ApiZenRequest)
class ApiZenRequestAdmin:
    fields = ('request_id', 'method', 'headers', 'name', 'path', 'querystring', 'payload', 'access_time',
              'status', 'code', 'success', 'message', 'response')
    readonly_fields = fields
    list_display = ('request_id', 'method', 'path', 'access_time', 'status', 'code')
    search_fields = ('request_id', 'method', 'name')
    list_filter = ('access_time',)



