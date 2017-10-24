#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/10/24 下午4:58
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : routing.py
# @Software: PyCharm

__author__ = 'blackmatrix'


def routing(request):
    # 获取请求参数
    args = request.GET or {}
    args.update(request.POST or {})

if __name__ == '__main__':
    pass
