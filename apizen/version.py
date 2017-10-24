#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/4 上午11:03
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : version.py
# @Software: PyCharm
import copy

__author__ = 'blackmatrix'

"""
-------------------------------
ApiZen 接口版本的注册、管理与继承功能
-------------------------------
适用版本：Flask、Tornado
-------------------------------
"""

allversion = {}


def version(v, enable=True):
    """
    Web Api版本注册
    :param v:  版本号
    :param enable:  版本是否停用
    :return:  无
    """
    def _version(cls):
        allversion.update({str(v): {'methods': cls, 'enable': enable}})
        return cls
    return _version


class _ApiMethodsMeta(type):

    def __new__(mcs, classname, supers, clsdict):
        # 破坏并重建继承关系
        new_api_methods = {}
        cls = type.__new__(mcs, classname, supers, clsdict)
        new_cls = type.__new__(mcs, classname, (object,), clsdict)
        if hasattr(cls, 'api_methods'):
            new_api_methods = copy.deepcopy(cls.api_methods)
        for super_ in cls.__mro__:
            if hasattr(super_, 'api_methods'):
                new_api_methods.update({key: value
                                        for key, value in getattr(super_, 'api_methods').items()
                                        if key not in new_api_methods})
        setattr(new_cls, 'api_methods', new_api_methods)
        del cls
        return new_cls

    def __init__(cls, classname, supers, clsdict):
        type.__init__(cls, classname, supers, clsdict)


class ApiMethodsBase(metaclass=_ApiMethodsMeta):
    api_methods = {}


if __name__ == '__main__':
    pass
