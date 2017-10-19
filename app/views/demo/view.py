#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/10/19 下午2:41
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : view.py
# @Software: PyCharm
from django.http import HttpResponse

__author__ = 'blackmatrix'


def hello(request):
    return HttpResponse("Hello world ! ")

if __name__ == '__main__':
    pass
