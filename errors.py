#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/10/24 下午4:00
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : errors.py
# @Software: PyCharm
import types
from json import JSONDecodeError
from toolkit.exceptions import SysException

__author__ = 'blackmatrix'

_no_value = object()


class Exceptions(ApiSysExceptions):
    # 非法的时间戳参数
    err_user_or_password = SysException(err_code=2001, http_code=404, err_msg='不存在的用户名或密码')


if __name__ == '__main__':
    pass
