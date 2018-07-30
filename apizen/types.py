#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/5/19 上午8:55
# @Author: Matrix
# @Site: apizen
# @File: types.py
# @Software: PyCharm
from .common.types import *

__author__ = 'blackmatrix'


class ApiRequest(TypeBase):

    typename = 'Request'

    def convert(self, *, value=None):
        return self.request

    def __init__(self, request=None):
        self.request = request
        super().__init__()
