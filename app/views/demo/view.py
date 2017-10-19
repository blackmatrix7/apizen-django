#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/10/19 下午2:41
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : view.py
# @Software: PyCharm
from app import settings
from django.shortcuts import render

__author__ = 'blackmatrix'


def hello(request):
    context = dict()
    context['hello'] = 'Hello World!'
    return render(request, 'demo/index.html', context)

if __name__ == '__main__':
    pass
