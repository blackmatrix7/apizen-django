#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/3/14 下午1:47
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: errors.py
# @Software: PyCharm
from toolkit.exceptions import SysException

__author__ = 'blackmatrix'


class Exceptions:
    # 非法的时间戳参数
    err_user_or_password = SysException(err_code=2001, http_code=404, err_msg='不存在的用户名或密码')

