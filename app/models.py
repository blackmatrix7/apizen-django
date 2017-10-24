#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/10/23 下午4:02
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : models.py
# @Software: PyCharm
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

__author__ = 'blackmatrix'


class BaseModel(models.Model):
    pass


class Users(BaseModel):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=256)

    @staticmethod
    def make_password(password):
        return make_password(password)

    def check_password(self, password):
        return check_password(password, encoded=self.password)
