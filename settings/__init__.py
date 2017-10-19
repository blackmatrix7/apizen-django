#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/10/19 下午3:58
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : __init__.py.py
# @Software: PyCharm
from toolkit.cmdline import cmdline

__author__ = 'blackmatrix'

settings = {'default': 'settings.default'}

current_settings = settings[cmdline.config]

if __name__ == '__main__':
    pass
