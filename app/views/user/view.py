#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/10/20 下午5:19
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : login.py
# @Software: PyCharm
import json
from app.models import Users
from django.shortcuts import render
from django.http import HttpResponse

__author__ = 'blackmatrix'


def sign_in(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = Users.objects.get(email=email)
        result = user.check_password(password)
        print(result)


def sign_up(request):
    """
    账户注册
    :param request:
    :return:
    """
    name = request.POST['fullname']
    email = request.POST['email']
    password = request.POST['password']
    rpassword = request.POST['rpassword']
    user = Users()
    user.name = name
    user.email = email
    user.password = user.make_password(password)
    user.save()
    resp = {'code': 1000, 'response': 'sign up success'}
    return HttpResponse(json.dumps(resp), content_type="application/json")


if __name__ == '__main__':
    pass
