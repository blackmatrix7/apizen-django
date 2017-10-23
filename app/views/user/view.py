#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/10/20 下午5:19
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : login.py
# @Software: PyCharm
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password

__author__ = 'blackmatrix'


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == "POST":
        pass


def sign_up(request):
    if request.method == "POST":
        pass


if __name__ == '__main__':
    pass
