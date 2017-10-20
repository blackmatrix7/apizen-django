#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/10/20 下午5:19
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : login.py
# @Software: PyCharm
from django.shortcuts import render

__author__ = 'blackmatrix'


def login(request):
    return render(request, 'user/login.html')

if __name__ == '__main__':
    pass
