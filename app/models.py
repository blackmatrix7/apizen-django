#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/10/23 下午4:02
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : models.py
# @Software: PyCharm
from django.db import models

__author__ = 'blackmatrix'


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=256)
